import { Issues, columns } from "./columns";
import { DataTable } from "./data_table";
import { ModeToggle } from "./mode_toggle";

type postPops = {
  url: string;
  analysis_type: string;
  num_issues: number;
  per_page: number;
};

const data_mock: postPops = {
  url: "https://github.com/vercel/next.js",
  analysis_type: "emotion",
  num_issues: 100,
  per_page: 100,
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

export default async function Home() {
  const data = await postData(data_mock);
  console.log(data[0].url);
  return (
    <div className="hidden h-full flex-1 flex-col space-y-8 p-8 md:flex">
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
      <DataTable columns={columns} data={data} />
    </div>
  );
}
