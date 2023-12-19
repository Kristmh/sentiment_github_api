"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Issues, columns } from "./columns";
import { DataTable } from "./data_table";
import { ModeToggle } from "./mode_toggle";
import React, { useState } from "react";
type postPops = {
  url: string;
  analysis_type: string;
  num_issues: number;
  per_page: number;
};

const data_mock_1: postPops = {
  url: "https://github.com/vercel/next.js",
  analysis_type: "emotion",
  num_issues: 2,
  per_page: 2,
};

async function postData(data: postPops): Promise<Issues[]> {
  const res = await fetch("http://127.0.0.1:8000/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to post data: ${res.status} ${errorText}`);
  }

  return res.json();
}

export default function Home() {
  const [url, setUrl] = useState<string>(""); // State to store the input value
  const [data, setData] = useState<Issues[]>([]); // State to hold fetched data

  const [sentimentValue, setSentimentValue] = useState<string>("sentiment"); // State for the radio button value

  const handleRadioChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSentimentValue(event.target.value); // Update state with radio button value
    console.log("Radio button changed to:", event.target.value); // Debugging line
  };
  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value); // Update state with input value
  };

  const handleButtonClick = async () => {
    // Process the Url value when the button is clicked
    // For example, sending it to a server:
    console.log("url to be processed:", url);
    console.log("Radio button value:", sentimentValue);

    const input_data: postPops = {
      url: url,
      analysis_type: sentimentValue,
      num_issues: 2,
      per_page: 2,
    };
    const fetchedData = await postData(input_data);
    setData(fetchedData); // Update the data state with fetched data

    // Clear the input field after processing
    setUrl("");
  };

  const handleButtonClickReset = async () => {
    setData([]);
  };
  return (
    <div className="hidden h-full flex-1 flex-col space-y-8 p-8 md:flex">
      <div className="flex full max-w-3xl items-center space-x-2">
        <Input
          type="url"
          placeholder="Enter a github repo e.g. https://github.com/neovim/neovim"
          value={url} // Set the input value from state
          onChange={handleUrlChange} // Update state on input change
        />
        <RadioGroup value={sentimentValue} onChange={handleRadioChange}>
          <div className="flex items-center space-x-2">
            <RadioGroupItem
              value="emotion"
              id="r1"
              checked={sentimentValue === "emotion"}
            />
            <Label htmlFor="r1">Emotion</Label>
          </div>
          <div className="flex items-center space-x-2">
            <RadioGroupItem
              value="sentiment"
              id="r2"
              checked={sentimentValue === "sentiment"}
            />
            <Label htmlFor="r2">Sentiment</Label>
          </div>
        </RadioGroup>
        <Button type="submit" onClick={handleButtonClick}>
          Submit
        </Button>
        <Button type="submit" onClick={handleButtonClickReset}>
          Reset
        </Button>
      </div>
      <div className="flex items-center justify-between space-y-2">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Github issues</h2>
          <p className="text-muted-foreground">
            List of github issuse with sentiment analysis.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <ModeToggle />
        </div>
      </div>
      {data.length > 0 && <DataTable columns={columns} data={data} />}
    </div>
  );
}
