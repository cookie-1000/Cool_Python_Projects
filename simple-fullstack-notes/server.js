import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const PORT = 3000;

// Needed because we’re in ES modules ("type": "module")
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// In-memory "database"
let notes = [
  {
    id: 1,
    text: "Hello! This is your first note.",
    createdAt: new Date().toISOString()
  }
];
let nextId = 2;

// API routes
app.get("/api/notes", (req, res) => {
  res.json(notes);
});

app.post("/api/notes", (req, res) => {
  const text = (req.body?.text ?? "").trim();
  if (!text) return res.status(400).json({ error: "text is required" });

  const newNote = {
    id: nextId++,
    text,
    createdAt: new Date().toISOString()
  };

  notes.unshift(newNote);
  res.status(201).json(newNote);
});

app.delete("/api/notes", (req, res) => {
  notes = [];
  nextId = 1;
  res.json({ ok: true });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
