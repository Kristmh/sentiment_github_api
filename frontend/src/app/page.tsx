import { Issues, columns } from "./columns"
import { DataTable } from "./data_table"

type postPops = {
  url: string;
  analysis_type: string;
  num_issues: number;
  per_page: number;
};

const data_mock: postPops = {
  url: "https://github.com/vercel/next.js",
  analysis_type: "emotion",
  num_issues: 2,
  per_page: 2,
};
async function postData(data: postPops) {
  const res = await fetch("http://127.0.0.1:8000/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    cache: "no-cache",
  });

  if (!res.ok) {
    throw new Error("Failed to post data");
  }

  return res.json();
}
export default async function Home() {
  const data = await postData(data_mock);
  const res = data[0].score;
  console.log(data[0].ulr);
  return (
    <div>
      <DataTable columns={columns} data={data} />
      <h1>hello world</h1>
      <h2>{res}</h2>
      <h2>{data[0].url}</h2>
      <h2>{data[0].title}</h2>
      <h2>{data[0].body}</h2>
      <h2>{data[0].results.score}</h2>
      <h2>{data[0].results.label}</h2>



    </div>
  );
}
