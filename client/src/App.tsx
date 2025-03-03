import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

"use client";
import {
  useRef,
  useState
} from "react";
import {
  toast
} from "sonner";
import {
  useForm
} from "react-hook-form";
import {
  zodResolver
} from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  cn
} from "@/lib/utils";
import {
  Button
} from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useDropzone } from "react-dropzone";
import { UploadCloud } from "lucide-react";
import { Input } from './components/ui/input';

const formSchema = z.object({
  fileInput: z.string(),
  model: z.string(),
  algorithm: z.string()
});

const FileUpload = ({ form }) => {
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  return (
    <FormField
      control={form.control}
      name="fileInput"
      render={({ field: { value, onChange, ...fieldProps } }) => (
        <FormItem>
          <FormLabel>Malware Sample</FormLabel>
          <FormControl>
            <div
              className={cn(
                "border-2 border-dashed border-gray-500 p-6 rounded-lg flex flex-col items-center justify-center cursor-pointer"
              )}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                onChange={(event) => {
                  const selectedFile = event.target.files && event.target.files[0];
                  if (selectedFile) {
                    setFile(selectedFile);
                    onChange(selectedFile);
                  }
                }}
              />
              <UploadCloud size={32} className="text-gray-400 mb-2" />
              <p className="text-sm text-gray-300 font-semibold">
                {file ? file.name : "Click to upload or drag and drop"}
              </p>
              <p className="text-xs text-gray-500">SVG, PNG, JPG, or GIF</p>
            </div>
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};

export default function MyForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });

  function onSubmit(values: any) {
    try {
      console.log(values);
      toast(
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(values, null, 2)}</code>
        </pre>
      );
    } catch (error) {
      console.error("Form submission error", error);
      toast.error("Failed to submit the form. Please try again.");
    }
  }

  const appStyle = {
    backgroundColor: '#f0f4f8', // Light gray background color
    minHeight: '100vh', // Ensures the background covers the full height of the screen
    display: 'flex', // Use flexbox for easy centering
    flexDirection: 'column', // Vertical layout
    justifyContent: 'center', // Center content vertically
    alignItems: 'center', // Center content horizontally
    padding: '20px',
  };

  const cardStyle = {
    width: '100%', // Ensure the card takes 100% of the parent's width (75% of screen width)
    backgroundColor: '#f7fafc', // Light gray background
    borderRadius: '8px', 
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    padding: '20px',
  };

  const headerStyle = {
    color: '#2d3748', // Dark gray for header text
    marginBottom: '20px',
  };

  const selectStyle = {
    backgroundColor: '#edf2f7', // Light gray for select dropdown
    borderColor: '#cbd5e0', // Subtle border color
    borderRadius: '8px',
    padding: '8px 12px',
    width: '100%',
  };

  const selectTriggerStyle = {
    backgroundColor: '#edf2f7',
    borderColor: '#cbd5e0',
    padding: '8px 12px',
    borderRadius: '8px',
    color: '#2d3748',
  };

  const buttonStyle = {
    backgroundColor: '#3182ce', // Blue color for button
    color: '#fff',
    padding: '12px 24px',
    borderRadius: '8px',
    cursor: 'pointer',
    border: 'none',
    transition: 'background-color 0.3s',
  };

  const buttonHoverStyle = {
    backgroundColor: '#2b6cb0', // Darker blue on hover
  };

  return (
    <div style={appStyle}>
      <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl" style={headerStyle}>
        Function Level Explanations of Malware
      </h1>

      <Card style={cardStyle}>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 max-w-3xl mx-auto py-10">
              <FileUpload form={form} />

              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '20px' }}>
                <FormField
                  control={form.control}
                  name="algorithm"
                  render={({ field }) => (
                    <FormItem style={{ flex: 1 }}>
                      <FormLabel>Algorithm</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value} style={selectStyle}>
                        <FormControl>
                          <SelectTrigger style={selectTriggerStyle}>
                            <SelectValue placeholder="LIME" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="LIME">Lime</SelectItem>
                          <SelectItem value="KERNEL SHAP">Kernel Shap</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="model"
                  render={({ field }) => (
                    <FormItem style={{ flex: 1 }}>
                      <FormLabel>Model</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value} style={selectStyle}>
                        <FormControl>
                          <SelectTrigger style={selectTriggerStyle}>
                            <SelectValue placeholder="FLEM_FUNCTIONS_ONLY" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="flem_functions_only">FUNCTIONS_ONLY</SelectItem>
                          <SelectItem value="flem_text_section">TEXT_SECTION</SelectItem>
                          <SelectItem value="flem_whole_exe">WHOLE_EXE</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button 
                type="submit" 
                style={buttonStyle} 
                className="hover:bg-blue-700 focus:outline-none transition"
              >
                Submit
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
