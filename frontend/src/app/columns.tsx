"use client"

import { ColumnDef } from "@tanstack/react-table"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Issues = {
  url: string
  title: string
  body: string
}

export const columns: ColumnDef<Issues>[] = [
  {
    accessorKey: "url",
    header: "Url",
  },
  {
    accessorKey: "title",
    header: "Title",
  },
  {
    accessorKey: "body",
    header: "Body",
  },
]
