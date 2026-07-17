import os
import re
import base64
import urllib.request
import urllib.error

def urlsafe_b64encode_str(s):
    # Encode a string to URL-safe base64 without padding
    encoded = base64.urlsafe_b64encode(s.encode('utf-8')).decode('ascii')
    return encoded

def download_mermaid_image(mermaid_code, output_path):
    encoded = urlsafe_b64encode_str(mermaid_code)
    url = f"https://mermaid.ink/img/{encoded}"
    print(f"Downloading from {url} to {output_path}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print("Download successful!")
        return True
    except urllib.error.URLError as e:
        print(f"Error downloading: {e}")
        return False

def main():
    workspace = r"d:\AIApplication\SS13"
    srs_path = os.path.join(workspace, "System_Design_SRS.md")
    assets_dir = os.path.join(workspace, "assets")
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created directory: {assets_dir}")
        
    with open(srs_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all mermaid code blocks
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
    matches = pattern.findall(content)
    
    if len(matches) < 2:
        print(f"Expected at least 2 mermaid blocks, found {len(matches)}.")
        return
        
    usecase_code = matches[0].strip()
    erd_code = matches[1].strip()
    
    usecase_img_path = os.path.join(assets_dir, "usecase.png")
    erd_img_path = os.path.join(assets_dir, "erd.png")
    
    # Download images
    success_usecase = download_mermaid_image(usecase_code, usecase_img_path)
    success_erd = download_mermaid_image(erd_code, erd_img_path)
    
    if success_usecase and success_erd:
        # Replace the first mermaid block with usecase.png
        # and the second with erd.png
        def replacer(match):
            nonlocal block_idx
            block_idx += 1
            if block_idx == 1:
                return "![Sơ đồ Use Case](assets/usecase.png)"
            elif block_idx == 2:
                return "![Sơ đồ ERD](assets/erd.png)"
            return match.group(0)
            
        block_idx = 0
        new_content = pattern.sub(replacer, content)
        
        with open(srs_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Updated System_Design_SRS.md with image references!")
    else:
        print("Failed to download one or both images. System_Design_SRS.md was not modified.")

if __name__ == "__main__":
    main()
