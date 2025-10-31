import * as XLSX from "xlsx";

/**
 * Parse uploaded dataset file and return column headers.
 * Supports CSV, TXT, and Excel (.xlsx/.xls) formats.
 *
 * @param {File} file - Uploaded dataset file.
 * @returns {Promise<{ columns: string[], rows: any[] }>}
 */
export async function parseDataset(file) {
  const ext = file.name.split(".").pop().toLowerCase();

  // Read file as binary string or text depending on type
  const data = await file.arrayBuffer();

  let columns = [];
  let rows = [];

  if (["xlsx", "xls"].includes(ext)) {
    const workbook = XLSX.read(data, { type: "array" });
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    rows = XLSX.utils.sheet_to_json(sheet, { defval: "" });
    if (rows.length > 0) {
      columns = Object.keys(rows[0]);
    }
  } else if (["csv", "txt"].includes(ext)) {
    const text = new TextDecoder("utf-8").decode(data);
    const lines = text.trim().split("\n");
    columns = lines[0].split(/[,\t]/).map((c) => c.trim());
    rows = lines.slice(1).map((line) => {
      const values = line.split(/[,\t]/);
      return Object.fromEntries(columns.map((c, i) => [c, values[i]]));
    });
  } else {
    throw new Error("Unsupported file type. Please upload CSV, TXT, or Excel.");
  }

  return { columns, rows };
}
