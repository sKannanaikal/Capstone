import { useLocation } from "react-router-dom";
import '../App.css';
import { TrendingUp } from "lucide-react"
import { Label, Pie, PieChart } from "recharts"
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent} from "@/components/ui/chart"
import { Bar, BarChart } from "recharts"
import { AlignLeft } from "lucide-react";
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import { googlecode } from "react-syntax-highlighter/dist/esm/styles/hljs";
import { XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import { extent, bin } from "d3-array";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
  
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";
import React from "react";

  export default function ResultsPage() {
    const location = useLocation();
    const data = location.state?.responseData || {}; 
    const assemblyCode = data.assemblyCode;
    const normalizedAttributions = data.normalizedAttributions;
    const rankedMaliciousFunctions = data.rankedMaliciousFunctions;
    const sortedAttributionIndexes = data.sortedAttributionIndexes;
    const rawAttributionScores = data.rawAttributionScores;
    const functionMapping = data.functionMapping;

    const NUM_BINS = 25;
   
    const validScores = rawAttributionScores[0]
  .flat() 
  .map(Number) 
  .filter((x) => !isNaN(x)); 

  const [minScore, maxScore] = extent(validScores);

  if (minScore === undefined || maxScore === undefined) {
    console.error("No valid data for histogram.");
    return [];
  }
  

  const binGenerator = bin()
  .domain([minScore, maxScore])
  .thresholds(NUM_BINS); 

    const bins = binGenerator(validScores);


    console.log(bins)


    let noCorrelation = 0;
    let malicious = 0;
    let benign = 0;

    for (let index = 0; index < rawAttributionScores[0].length; index++) {
      let score = parseFloat(rawAttributionScores[0][index]);

      if(score == 0.0) {
        noCorrelation += 1;
      }
      else if (score > 0.0) {
        malicious += 1;
      }

      else {
        benign += 1;
      }
      
    }

    const topFive = [];
    for (let i = 0; i < 5; i++) {
        topFive[i] = rankedMaliciousFunctions[i];
      } 
   

      const chartData = bins.map((b) => ({
        range: `${b.x0?.toFixed(2)} - ${b.x1?.toFixed(2)}`,
        count: b.length ?? 0, 
      }));
      
      const pieChartData = [
        { functionClass: "malicious", functions: malicious, fill: "var(--color-malicious)" },
        { functionClass: "benign", functions: benign, fill: "var(--color-benign)" },
        { functionClass: "no_correlation", functions: noCorrelation, fill: "var(--color-no_correlation)" },
      ]

      const totalFunctions = malicious + noCorrelation + benign;
    

      const chartConfig = {
        count: {
          label: "Attribution Scores",
          color: "#2563eb",
        },
      } satisfies ChartConfig;

      const pieChartConfig = {
        functions: {
          label: "Functions",
        },
        malicious: {
          label: "malicious",
          color: "hsl(var(--chart-1))",
        },
        benign: {
          label: "benign",
          color: "hsl(var(--chart-2))",
        },
        no_correlation: {
          label: "No Correlation",
          color: "hsl(var(--chart-3))",
        },
      } satisfies ChartConfig
      
      
  
    return (
      <div className="p-8 w-full min-h-screen text-black">

        <h1 className="text-6xl font-bold mb-6">Analysis Results</h1>

        <Separator className="w-full h-1 bg-gray-800" />

        <h2 className="text-3xl font-bold mb-6 mt-6">Top 5 Malicious Functions</h2>

        <div className="flex h=[10vw] w-[90vw] gap-2 items-center justify-center">

        {topFive.map((title, index) => (
            <Card key={index} className="h-[10vw] w-1/5 flex items-center justify-center border-2 border-gray-300">
            <CardHeader className="text-center">
                <CardTitle className="text-4xl font-bold">{title}</CardTitle>
            </CardHeader>
            </Card>
        ))}
        </div>

<div className="mt-[2vw]"> 

<h2 className="text-3xl font-bold mb-6">Function Data Overview</h2>

  <ScrollArea className="h-[30vw] w-[90vw] rounded-md border p-4">
    <Table className="h-full w-full text-black border-2 border-gray-400">
      <TableHeader>
        <TableRow>
          <TableHead className="text-center text-xl">Index</TableHead>
          <TableHead className="text-center text-xl">Function Name</TableHead>
          <TableHead className="text-center text-xl">Attribution Score</TableHead>
          <TableHead className="text-center text-xl">Function Length</TableHead>
          <TableHead className="text-center text-xl">Function Offsets</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Array.from({ length: rankedMaliciousFunctions.length }).map((_, i) => (
          <>
            <TableRow key={`row1-${i}`}>
              <TableCell className="text-center text-xl">{i + 1}</TableCell>
              <TableCell className="text-center text-xl">{rankedMaliciousFunctions[i]}</TableCell>
              <TableCell className="text-center text-xl">{normalizedAttributions[sortedAttributionIndexes[i]]*100}</TableCell>
              <TableCell className="text-center text-xl">{parseInt(functionMapping[rankedMaliciousFunctions[i]][1], 16) - parseInt(functionMapping[rankedMaliciousFunctions[i]][0], 16)}</TableCell>
              <TableCell className="text-center text-xl">({parseInt(functionMapping[rankedMaliciousFunctions[i]][0], 16)}, {parseInt(functionMapping[rankedMaliciousFunctions[i]][1], 16)})</TableCell>
            </TableRow>
          </>
        ))}
      </TableBody>
    </Table>
  </ScrollArea>
</div>

<h2 className="text-3xl font-bold mb-6">Analysis Statistics</h2>

<div className="mt-[2vw] w-[90vw] flex">

<ChartContainer config={chartConfig} className="min-h-[300px] w-full">
  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={chartData}>

    <text 
      x="50%" 
      y="20" 
      textAnchor="middle" 
      dominantBaseline="hanging" 
      fontSize="16" 
      fontWeight="bold"
    >
      Attribution Score Distribution
    </text>
      <CartesianGrid strokeDasharray="3 3" />

      <XAxis 
    dataKey="range" 
    angle={-30}
    textAnchor="end"
    interval={Math.ceil(chartData.length / 6)} 
    tick={{ fontSize: 12 }}
    height={50} 
    padding={{ left: 10, right: 10 }} 
    label={{ 
      value: "Attribution Score Ranges", 
      position: "insideBottom", 
      dy: 30,
      style: { fontSize: 14, fill: "#666" } 
  }}
/>

      <YAxis 
        label={{ value: "Number of Functions", angle: -90, position: "insideLeft", dy: -10 }}
      />


      <Tooltip formatter={(value, name) => [`${value} functions`, name]} />

      <Bar dataKey="count" fill="var(--color-count)" radius={4} />
    </BarChart>
  </ResponsiveContainer>
</ChartContainer>

    <ChartContainer
          config={pieChartConfig}
          className="min-h-[200px] w-full"
        >
          <PieChart>
          <text 
      x="50%" 
      y="20" 
      textAnchor="middle" 
      dominantBaseline="hanging" 
      fontSize="16" 
      fontWeight="bold"
    >
      Function Categorization
    </text>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={pieChartData}
              dataKey="functions"
              nameKey="functionClass"
              innerRadius={60}
              strokeWidth={5}
            >
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text
                        x={viewBox.cx}
                        y={viewBox.cy}
                        textAnchor="middle"
                        dominantBaseline="middle"
                      >
                        <tspan
                          x={viewBox.cx}
                          y={viewBox.cy}
                          className="fill-foreground text-3xl font-bold"
                        >
                          {totalFunctions.toLocaleString()}
                        </tspan>
                        <tspan
                          x={viewBox.cx}
                          y={(viewBox.cy || 0) + 24}
                          className="fill-muted-foreground"
                        >
                          Functions
                        </tspan>
                      </text>
                    )
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
</div>
    <div className="mt-16">
        <h2 className="text-3xl font-bold mb-6">Assembly Code Example</h2>
        
        <ScrollArea className="h-[30vw] w-[90vw] rounded-md border p-4">
        <SyntaxHighlighter language="asm" style={googlecode} className="text-left">
          {assemblyCode}
        </SyntaxHighlighter>
        </ScrollArea>
      </div>

      </div>
    );
}
