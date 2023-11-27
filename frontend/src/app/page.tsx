type postPops = {
  url: string;
  analysis_type: string;
};

const data_mock: postPops = {
  url: "https://github.com/vercel/next.js",
  analysis_type: "emotion",
};
async function postData(data: postPops) {
  const res = await fetch("http://127.0.0.1:8000/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    throw new Error("Failed to post data");
  }

  return res.json();
}
export default async function Home() {
  const data = await postData(data_mock);
  const results = data["results"];
  const sentiment = results[0]["sentiment"];
  console.log(data);
  console.log(sentiment);
  return (
    <main>
      <div>{data.url}</div>
      <div>{data.analysis}</div>
      <div>{results[0].issue}</div>
      <div>{sentiment[0]["score"]}</div>
      <div>{sentiment[0]["label"]}</div>
      <h1>Repo: {data.url}</h1>
      <table>
        <thead>
          <tr>
            <th>URL</th>
            <th>Analysis</th>
            <th>Issue</th>
            <th>Score</th>
            <th>Label</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, index) => {
            const sentiment = result["sentiment"];
            return (
              <tr key={index}>
                <td>{data.analysis_type}</td>
                <td>{result.issue}</td>
                <td>{sentiment[0]["score"]}</td>
                <td>{sentiment[0]["label"]}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </main>
  );
}
