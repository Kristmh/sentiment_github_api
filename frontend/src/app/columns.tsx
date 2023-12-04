"use client"

import { ColumnDef } from "@tanstack/react-table"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Issues = {
  url: string
  title: string
  body: string
  score: string
  label: string
  pull_request: string
}

export const columns: ColumnDef<Issues>[] = [
  {
    accessorKey: "score",
    header: "Score",
  },
  {
    accessorKey: "label",
    header: "Label",
  },
  {
    accessorKey: "title",
    header: "Title",
  },
  {
    accessorKey: "body",
    header: "Body",
  },
  {
    accessorKey: "pull_request",
    header: "Pull Request",
  },
  {
    accessorKey: "url",
    header: "Url",
  },
]
