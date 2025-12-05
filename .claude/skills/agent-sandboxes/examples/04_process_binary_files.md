# Example 4: Process Binary Files

**When to use**: Uploading, processing, or downloading binary files (images, PDFs, executables).

## Workflow

```bash
# Initialize sandbox
uv run sbx init
# Capture sandbox_id from output

# Upload the binary file
uv run sbx files upload <sandbox_id> ./input.jpg /home/user/input.jpg

# Install processing library
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system pillow"

# Process the file
uv run sbx files write <sandbox_id> /home/user/resize.py "from PIL import Image; img = Image.open('/home/user/input.jpg'); img.resize((800,600)).save('/home/user/output.jpg')"
uv run sbx exec <sandbox_id> "python3 /home/user/resize.py"

# Download the result
uv run sbx files download <sandbox_id> /home/user/output.jpg ./output.jpg
```

## Key Points

- **Use `upload`/`download` for binary files** (images, PDFs, executables)
- **Use `write`/`read` for text files only**
- Common libraries: `pillow` (images), `reportlab`/`pypdf2` (PDFs)

## Supported Binary Types

Images (jpg, png, gif, webp), Documents (pdf, docx, xlsx), Archives (zip, tar, gz), Executables
