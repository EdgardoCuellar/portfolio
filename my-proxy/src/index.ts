import { fromHono } from "chanfana";
import { Hono } from "hono";
import { TaskCreate } from "./endpoints/taskCreate";
import { TaskDelete } from "./endpoints/taskDelete";
import { TaskFetch } from "./endpoints/taskFetch";
import { TaskList } from "./endpoints/taskList";

// simple proxy worker: forward POST bodies to OpenRouter, injecting secret
// this keeps the API key out of the browser.
export default {
  async fetch(request: Request, env: Env) {
    // respond to CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          // allow the custom headers used by widget
          "Access-Control-Allow-Headers": "Content-Type, X-Title, HTTP-Referer",
        },
      });
    }
    if (request.method !== "POST") {
      return new Response("Method not allowed", {status:405});
    }
    // forward body to OpenRouter with the secret injected
    const proxied = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.OPENROUTER_KEY}`,
        "Content-Type": "application/json",
      },
      body: await request.text(),
    });
    // copy CORS header from upstream as well
    const respHeaders = new Headers(proxied.headers);
    respHeaders.set("Access-Control-Allow-Origin", "*");
    return new Response(proxied.body, {
      status: proxied.status,
      headers: respHeaders,
    });
  },
};
