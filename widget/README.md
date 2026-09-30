# KKR Chatbot — Chat Widget

The end-user chat widget for the KKR Chatbot platform. Built with **React 19 + TypeScript + Vite**, it communicates with the FastAPI backend and renders a fully interactive chat UI.

---

## Overview

| Detail | Value |
|---|---|
| Dev server | `http://localhost:5173` |
| Framework | React 19 + TypeScript |
| Bundler | Vite 8 |
| Styling | Tailwind CSS |
| Markdown | `react-markdown` + `remark-gfm` |

---

## Structure

```
widget/
├── src/
│   ├── App.tsx                 # Root component — session init, localStorage persistence, layout
│   ├── components/
│   │   ├── ChatWindow.tsx      # Scrollable message list with markdown rendering per bot reply
│   │   ├── MessageInput.tsx    # Textarea + send button; handles Enter-to-send
│   │   └── QuickActions.tsx    # Config-driven buttons rendered from /session/start response
│   ├── hooks/
│   │   └── useChat.ts          # API client: POST /message, session management
│   ├── types.ts                # Shared TypeScript interfaces (Message, QuickAction, Trace, etc.)
│   ├── App.css                 # Global styles
│   └── index.css               # Tailwind base imports
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── package.json
├── vite.config.ts              # strictPort: true → port 5173 only
├── tailwind.config.ts
└── tsconfig.json
```

---

## Development

```powershell
# From the widget/ directory:
npm install
npm run dev       # starts at http://localhost:5173

# Build for production:
npm run build     # outputs to widget/dist/

# Lint:
npm run lint      # runs oxlint
```

The backend API must be running at `http://localhost:8080` before the widget can send or receive messages. See the root [README](../README.md#running-locally) for full startup instructions.

---

## Key Behaviours

- **Session persistence** — `session_id` is stored in `localStorage` so the user's session survives page refreshes. The full conversation history is also stored in `localStorage` and restored on load.
- **Quick actions** — buttons are driven entirely by the `quick_actions` array returned from `POST /session/start`. No hardcoded labels exist in the widget code.
- **Markdown rendering** — bot replies are rendered as Markdown (bold, lists, links, tables) using `react-markdown` with the `remark-gfm` plugin.
- **Debug trace** — each bot reply includes a collapsible trace section showing `handler`, `classification`, RAG `scores`/`sources`, `llm_model`, `grounded`, and `duration_ms`. This is a development/QA aid and should be hidden or removed before production.
- **Clear cache** — the 🗑️ button calls `POST /session/clear-cache` with the current `session_id`, wiping both the response cache and session memory on the server, and clears `localStorage` on the client.

---

## Environment

The widget calls the backend at a hardcoded `http://localhost:8080` base URL during development. For production deployments, update the API base URL in `src/hooks/useChat.ts` or inject it via a Vite environment variable (`VITE_API_BASE_URL`).
