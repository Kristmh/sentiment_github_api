type Testing = {
  message: string;
};
async function getData() {
  const res = await fetch("http://127.0.0.1:8000/api/python", {
    cache: "no-cache",
  });

  //const res = await fetch("https://api.github.com/repos/vercel/next.js");
  // The return value is *not* serialized
  // You can return Date, Map, Set, etc.

  if (!res.ok) {
    // This will activate the closest `error.js` Error Boundary
    throw new Error("Failed to fetch data");
  }

  return res.json();
}
export default async function Home() {
  const data: Testing = await getData();
  console.log(data);
  return <div>{data.message}</div>;
}
