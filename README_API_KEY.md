# NCBI API Key Support

This fork adds support for NCBI API keys to improve rate limits and performance.

## Rate Limits

- **Without API key**: 3 requests per second
- **With API key**: 10 requests per second
- **Enhanced rate**: Available upon request to NCBI

## Setup

1. **Get an API Key** (optional but recommended):
   - Go to https://www.ncbi.nlm.nih.gov/account/settings/
   - Create an NCBI account if you don't have one
   - Generate an API key in your account settings

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. **Set Environment Variables**:
   ```bash
   export NCBI_API_KEY=your_api_key_here
   export NCBI_EMAIL=your_email@example.com  # optional
   ```

## Claude Desktop Configuration

Update your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "python3.11",
      "args": ["/path/to/PubMed-MCP-Server-Fork/pubmed_server.py"],
      "env": {
        "NCBI_API_KEY": "your_api_key_here",
        "NCBI_EMAIL": "your_email@example.com"
      }
    }
  }
}
```

## Benefits

- ✅ Higher rate limits (3 → 10 requests/sec)
- ✅ Better performance for intensive searches
- ✅ Compliance with NCBI guidelines
- ✅ Backward compatible (works without API key)

## Original Repository

This is a fork of [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) with added API key support.