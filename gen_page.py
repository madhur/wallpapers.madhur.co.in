import os
import glob
from PIL import Image
import shutil

def generate_html():
    horizontal_folders = ['morning', 'day', 'evening', 'night', 'midnight' ]
    vertical_folders = ['vertical/morning', 'vertical/day', 'vertical/evening', 'vertical/night', 'vertical/midnight']
    thumbnail_dir = 'thumbnails'
    
    # Create thumbnails directory if it doesn't exist
    if os.path.exists(thumbnail_dir):
        shutil.rmtree(thumbnail_dir)
    os.makedirs(thumbnail_dir)

    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Madhur's Wallpaper Gallery</title>

        <!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EWPKDCPRNG"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-EWPKDCPRNG');
</script>

        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background-color: #121212; 
                color: #e0e0e0;
            }
            h1, h2 { color: #ffffff; }
            .gallery { display: flex; flex-wrap: wrap; gap: 10px; }
            .thumbnail { 
                width: 200px; 
                height: 112px; 
                object-fit: cover; 
                cursor: pointer; 
                border: 2px solid #333;
                transition: border-color 0.3s ease;
            }
            .thumbnail:hover {
                border-color: #4CAF50;
            }
            .thumbnail.vertical { width: 100px; height: 178px; } /* Increased size for vertical thumbnails */
            .fullscreen { 
                display: none; 
                position: fixed; 
                top: 0; 
                left: 0; 
                width: 100%; 
                height: 100%; 
                background-color: rgba(0,0,0,0.9); 
                z-index: 100; 
            }
            .fullscreen img { 
                max-width: 90%; 
                max-height: 90%; 
                position: absolute; 
                top: 50%; 
                left: 50%; 
                transform: translate(-50%, -50%); 
            }
            .close { 
                position: absolute; 
                top: 15px; 
                right: 35px; 
                color: #f1f1f1; 
                font-size: 40px; 
                font-weight: bold; 
                cursor: pointer; 
            }
            .switch { 
                display: flex; 
                justify-content: center; 
                margin-bottom: 20px; 
            }
            .switch button { 
                padding: 10px 20px; 
                font-size: 16px; 
                cursor: pointer; 
                background-color: #333; 
                color: #e0e0e0; 
                border: none; 
                margin: 0 5px;
                transition: background-color 0.3s ease;
            }
            .switch button:hover {
                background-color: #555;
            }
            .active { 
                background-color: #4CAF50 !important; 
                color: white; 
            }
                    .github-ribbon {
                position: fixed;
                top: 0;
                right: 0;
                z-index: 9999;
            }
            .github-ribbon a {
                display: block;
                font-size: 13px;
                line-height: 20px;
                color: #fff;
                background-color: #4CAF50;
                text-decoration: none;
                text-align: center;
                padding: 5px 40px;
                transform: rotate(45deg);
                transform-origin: 45px 45px;
                box-shadow: 0 0 0 1px #1a7f37 inset,
                            0 5px 20px rgba(0,0,0,.3);
            }
        </style>
    </head>
    <body>

    
  <div class="github-ribbon">
            <a href="https://github.com/madhur/wallpapers.madhur.co.in">Fork me on GitHub</a>
        </div>
        <h1>Wallpaper Gallery</h1>
        <div class="switch">
            <button onclick="showGallery('horizontal')" id="horizontalBtn" class="active">Horizontal</button>
            <button onclick="showGallery('vertical')" id="verticalBtn">Vertical</button>
        </div>
    '''

    def process_folders(folders, gallery_id, is_vertical=False):
        content = f'<div id="{gallery_id}" class="gallery-container">'
        for folder in folders:
            content += f'<h2>{folder.split("/")[-1].capitalize()}</h2><div class="gallery">'
            for image_path in glob.glob(f'{folder}/*.jpg') + glob.glob(f'{folder}/*.png') + glob.glob(f'{folder}/*.webp'):
                thumbnail_path = os.path.join(thumbnail_dir, f'thumb_{os.path.basename(image_path)}')
                with Image.open(image_path) as img:
                    if is_vertical:
                        img.thumbnail((100, 178))  # Increased thumbnail size for vertical images
                    else:
                        img.thumbnail((200, 112))
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        img = img.convert('RGBA')
                        img.save(thumbnail_path, "PNG")
                    else:
                        img = img.convert('RGB')
                        img.save(thumbnail_path, "JPEG", quality=85)
                
                thumbnail_class = "thumbnail vertical" if is_vertical else "thumbnail"
                content += f'''
                <img src="{thumbnail_path}" alt="{os.path.basename(image_path)}" class="{thumbnail_class}" 
                     onclick="openFullscreen('{image_path}')">
                '''
            content += '</div>'
        content += '</div>'
        return content

    html_content += process_folders(horizontal_folders, "horizontalGallery")
    html_content += process_folders(vertical_folders, "verticalGallery", is_vertical=True)

    html_content += '''
        <div id="fullscreenView" class="fullscreen">
            <span class="close" onclick="closeFullscreen()">&times;</span>
            <img id="fullscreenImage">
        </div>

        <script>
        function openFullscreen(imagePath) {
            document.getElementById('fullscreenImage').src = imagePath;
            document.getElementById('fullscreenView').style.display = 'block';
            // Track fullscreen image view
            gtag('event', 'view_item', {
                'item_name': imagePath
            });
        }
        function closeFullscreen() {
            document.getElementById('fullscreenView').style.display = 'none';
        }

          function showGallery(type) {
            document.getElementById('horizontalGallery').style.display = type === 'horizontal' ? 'block' : 'none';
            document.getElementById('verticalGallery').style.display = type === 'vertical' ? 'block' : 'none';
            document.getElementById('horizontalBtn').classList.toggle('active', type === 'horizontal');
            document.getElementById('verticalBtn').classList.toggle('active', type === 'vertical');
            // Track gallery type switch
            gtag('event', 'select_content', {
                'content_type': 'gallery',
                'item_id': type
            });
        }

        // Initialize the view
        showGallery('horizontal');
        </script>
    </body>
    </html>
    '''

    with open('wallpaper_gallery.html', 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html()