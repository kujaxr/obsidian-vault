# -*- coding: utf-8 -*-
"""
知识库管理器 - 将网页/图片转换为带图文的MD笔记
"""

import os
import re
import json
import base64
import requests
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from readability.readability import Document
import html2text
from markdownify import markdownify as md_convert
import urllib.parse

# 知识库根目录
KB_ROOT = r"D:\知识库"

# 当前月份文件夹
CURRENT_MONTH = datetime.now().strftime('%Y-%m')

def sanitize_filename(name):
    """清理文件名，去除非法字符"""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip()[:50]
    return name or "untitled"

def get_article_folder(kb_root, title):
    """根据标题确定保存文件夹"""
    # 自动分类关键词
    categories = {
        'AI': ['AI', '人工智能', 'ChatGPT', 'GPT', 'LLM', '大模型', 'AIGC'],
        '汽车': ['汽车', '电动车', '智驾', '自动驾驶', '新能源', '电车', '特斯拉', '比亚迪', '华为'],
        '科技': ['科技', '手机', '芯片', '半导体', '硬件', 'Apple', 'iPhone'],
        '财经': ['财经', '投资', '股票', '基金', '经济', '金融'],
        '汽车技术': ['发动机', '底盘', '车身', '电池', '电机', '电控', '零部件'],
    }
    
    title_lower = title.lower()
    for cat, keywords in categories.items():
        if any(k.lower() in title_lower for k in keywords):
            return cat
    
    return CURRENT_MONTH

def download_image(img_url, folder, article_folder):
    """下载图片到本地，返回相对路径"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(img_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
        
        # 提取扩展名
        ext = resp.headers.get('content-type', '').split('/')[-1]
        if 'jpeg' in ext:
            ext = 'jpg'
        ext = ext.split(';')[0].strip()
        if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            ext = 'jpg'
        
        # 生成文件名
        img_name = f"{datetime.now().strftime('%H%M%S')}_{len(img_url) % 1000}.{ext}"
        img_path = os.path.join(folder, article_folder, 'images', img_name)
        
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        with open(img_path, 'wb') as f:
            f.write(resp.content)
        
        # 返回相对路径
        return f"images/{img_name}"
    except Exception as e:
        print(f"Download image failed: {e}")
        return None

def extract_images_from_html(html, folder, article_folder):
    """从HTML中提取图片，下载到本地"""
    soup = BeautifulSoup(html, 'lxml')
    images = []
    
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or img.get('data-original')
        if not src:
            continue
        
        # 跳过小图标和base64图片
        if src.startswith('data:') or 'icon' in src.lower():
            continue
        
        # 转换为绝对URL
        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/'):
            continue  # 相对路径跳过
        
        local_path = download_image(src, folder, article_folder)
        if local_path:
            images.append({'original': src, 'local': local_path})
            # 替换HTML中的图片地址
            img['src'] = local_path
    
    return soup, images

def url_to_filename(url):
    """从URL生成文件名"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip('/')
    if path:
        name = path.split('/')[-1]
        if '.' in name:
            name = name.rsplit('.', 1)[0]
    else:
        name = parsed.netloc
    
    return sanitize_filename(name)

def fetch_and_convert(url):
    """抓取网页并转换为Markdown"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    resp = requests.get(url, headers=headers, timeout=15)
    resp.encoding = resp.apparent_encoding or 'utf-8'
    
    # 解析标题
    soup = BeautifulSoup(resp.text, 'lxml')
    
    # 尝试多种方式获取标题
    title = None
    for tag in ['h1', 'article h1', '.title', '.article-title', '[class*="title"]', 'title']:
        if tag == 'title':
            title = soup.title.string if soup.title else None
        else:
            el = soup.select_one(tag)
            if el:
                title = el.get_text(strip=True)
        if title:
            break
    
    if not title:
        title = url_to_filename(url)
    
    # 使用readability提取正文
    try:
        doc = Document(resp.text)
        html_content = doc.summary()
        article_title = doc.title() or title
        if article_title and len(article_title) > len(title):
            title = article_title
    except:
        # fallback: 用整个HTML
        html_content = resp.text
        # 去掉script和style
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        html_content = str(soup)
    
    # 处理图片
    folder = KB_ROOT
    article_folder = get_article_folder(KB_ROOT, title)
    os.makedirs(os.path.join(folder, article_folder, 'images'), exist_ok=True)
    
    soup_content, images = extract_images_from_html(html_content, folder, article_folder)
    
    # 转换为Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.image_links = True
    h.unicode_snob = True
    h.body_width = 0  # 不换行
    
    md_content = h.handle(str(soup_content))
    
    return {
        'title': title,
        'url': url,
        'content': md_content,
        'images': images,
        'folder': article_folder
    }

def save_as_md(data, custom_title=None):
    """保存为MD文件"""
    title = custom_title or data['title']
    folder = data['folder']
    
    # 创建月份文件夹
    month_folder = os.path.join(KB_ROOT, CURRENT_MONTH)
    os.makedirs(month_folder, exist_ok=True)
    os.makedirs(os.path.join(month_folder, 'images'), exist_ok=True)
    
    # 生成文件名
    safe_title = sanitize_filename(title)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_title}.md"
    filepath = os.path.join(month_folder, filename)
    
    # 生成MD文件头部
    md_header = f"""---
title: {title}
source: {data.get('url', 'unknown')}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags: []
---

# {title}

> 原文链接：{data.get('url', '')}

"""
    
    # 组装完整MD
    full_md = md_header + data['content']
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_md)
    
    return {
        'filepath': filepath,
        'filename': filename,
        'folder': CURRENT_MONTH,
        'title': title
    }

def save_image(image_path, custom_title=None):
    """保存图片为笔记"""
    try:
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        # 读取图片尺寸
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(img_data))
        w, h = img.size
        
        # 生成文件名
        if custom_title:
            safe_title = sanitize_filename(custom_title)
        else:
            safe_title = f"截图_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 保持原扩展名
        ext = os.path.splitext(image_path)[1] or '.png'
        filename = f"{safe_title}{ext}"
        
        month_folder = os.path.join(KB_ROOT, CURRENT_MONTH)
        os.makedirs(month_folder, exist_ok=True)
        os.makedirs(os.path.join(month_folder, 'images'), exist_ok=True)
        
        filepath = os.path.join(month_folder, filename)
        
        with open(filepath, 'wb') as f:
            f.write(img_data)
        
        return {
            'filepath': filepath,
            'filename': filename,
            'folder': CURRENT_MONTH,
            'size': f"{w}x{h}"
        }
    except Exception as e:
        return {'error': str(e)}

def save_text(text, custom_title=None):
    """保存文本为笔记"""
    title = custom_title or f"文本笔记_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    month_folder = os.path.join(KB_ROOT, CURRENT_MONTH)
    os.makedirs(month_folder, exist_ok=True)
    
    safe_title = sanitize_filename(title)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_title}.md"
    filepath = os.path.join(month_folder, filename)
    
    md_content = f"""---
title: {title}
created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags: []
---

# {title}

{text}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return {
        'filepath': filepath,
        'filename': filename,
        'folder': CURRENT_MONTH,
        'title': title
    }

def search_notes(keyword):
    """搜索笔记"""
    results = []
    for root, dirs, files in os.walk(KB_ROOT):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8') as fp:
                        content = fp.read()
                        if keyword.lower() in content.lower():
                            results.append({
                                'file': f,
                                'path': filepath,
                                'preview': content[:200]
                            })
                except:
                    pass
    return results

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Knowledge Base Manager")
        print("Usage:")
        print("  python kb_manager.py fetch <url> [title]  - Fetch and save article")
        print("  python kb_manager.py search <keyword>    - Search notes")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == 'fetch' and len(sys.argv) >= 3:
        url = sys.argv[2]
        title = sys.argv[3] if len(sys.argv) > 3 else None
        print(f"Fetching: {url}")
        data = fetch_and_convert(url)
        result = save_as_md(data, title)
        print(f"Saved: {result['filepath']}")
    
    elif cmd == 'search' and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        results = search_notes(keyword)
        print(f"Found {len(results)} results:")
        for r in results:
            print(f"  - {r['file']}")
    
    else:
        print("Unknown command")
