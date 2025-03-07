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

    const topFive = [];
    for (let i = 0; i < 5; i++) {
        topFive[i] = rankedMaliciousFunctions[sortedAttributionIndexes[i]];
      } 
   

    const chartData = [
        { month: "January", desktop: 186, mobile: 80 },
        { month: "February", desktop: 305, mobile: 200 },
        { month: "March", desktop: 237, mobile: 120 },
        { month: "April", desktop: 73, mobile: 190 },
        { month: "May", desktop: 209, mobile: 130 },
        { month: "June", desktop: 214, mobile: 140 },
      ]

      const pieChartData = [
        { functionClass: "malicious", functions: 275, fill: "var(--color-malicious)" },
        { functionClass: "benign", functions: 200, fill: "var(--color-benign)" },
        { functionClass: "no_correlation", functions: 287, fill: "var(--color-no_correlation)" },
      ]

      const totalFunctions = React.useMemo(() => {
        return pieChartData.reduce((acc, curr) => acc + curr.functions, 0)
      }, [])
    

      const chartConfig = {
        desktop: {
          label: "Desktop",
          color: "#2563eb",
        },
      } satisfies ChartConfig

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

<div className="mt-[2vw]"> {/* Added margin-top for gap */}

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
        {Array.from({ length: 20 }).map((_, i) => (
          <>
            <TableRow key={`row1-${i}`}>
              <TableCell className="text-center text-xl">1</TableCell>
              <TableCell className="text-center text-xl">FUN_001</TableCell>
              <TableCell className="text-center text-xl">2.14</TableCell>
              <TableCell className="text-center text-xl">50</TableCell>
              <TableCell className="text-center text-xl">16 - 30</TableCell>
            </TableRow>
            <TableRow key={`row2-${i}`}>
              <TableCell className="text-center text-xl">2</TableCell>
              <TableCell className="text-center text-xl">FUN_002</TableCell>
              <TableCell className="text-center text-xl">2.04</TableCell>
              <TableCell className="text-center text-xl">40</TableCell>
              <TableCell className="text-center text-xl">50 - 90</TableCell>
            </TableRow>
          </>
        ))}
      </TableBody>
    </Table>
  </ScrollArea>
</div>

<h2 className="text-3xl font-bold mb-6">Analysis Statistics</h2>

<div className="mt-[2vw] w-[90vw] flex">

    <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
      <BarChart accessibilityLayer data={chartData}>
        <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
      </BarChart>
    </ChartContainer>

    <ChartContainer
          config={pieChartConfig}
          //className="mx-auto aspect-square max-h-[250px]"
          className="min-h-[200px] w-full"
        >
          <PieChart>
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
