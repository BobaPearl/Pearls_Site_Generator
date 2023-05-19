import os
import yaml
import glob
import shutil
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from dateutil import tz
from markdown.extensions.nl2br import Nl2BrExtension

def read_front_matter(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading front matter file: {e}")
        return None

def read_site_info(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading site info file: {e}")
        return None
    
def read_header_links(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading header links file: {e}")
        return None
def read_custom_html(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: 'custom_html.yaml' file not found. Skipping custom HTML insertion.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error: Improperly formatted 'custom_html.yaml'. Skipping custom HTML insertion. Details: {e}")
        return {}
# Read YAML file and return a list of dictionaries
def read_yaml_file(filename):
    try:
        with open(filename, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return None

# Usage example:
#custom_html_data = read_custom_html("custom_html.yaml")

# Generate a string of HTML for navigation
def generate_navigation_yaml(yaml_data):
    nav_html = '<div id="nav">\n'
    for item in yaml_data:
        nav_html += f'<a href="{item["link"]}"> {item["name"]} </a> | '
    nav_html = nav_html.rstrip(' | ')  # remove the trailing separator
    nav_html += '\n</div>'
    return nav_html

def generate_navigation(current_page, max_page_key):
    def page_url(page_key):
        return f'{page_key}.html'

    current_page_int = int(current_page)
    prev_page_key = f'{max(current_page_int - 1, 1):03d}'
    next_page_key = f'{min(current_page_int + 1, int(max_page_key)):03d}'

    return f'''
<div class="comicNav">
    <a href="{page_url("001")}"><img src="/img/comicnav/nav_first.png" alt="First"></a>
    <a href="{page_url(prev_page_key)}"><img src="/img/comicnav/nav_previous.png" alt="Previous"></a>
    <a href="{page_url(next_page_key)}"><img src="/img/comicnav/nav_next.png" alt="Next"></a>
    <a href="{page_url(max_page_key)}"><img src="/img/comicnav/nav_last.png" alt="Last"></a>
</div>
'''

def generate_html(front_matter, site_info, image_folder='assets'):
    custom_html_data = read_custom_html("custom_html.yaml")
    header_links = read_header_links("header.yaml")
    last_generated_file = ""
    for key, metadata in sorted(front_matter.items()):  # Make sure the front_matter items are sorted
        file_prefix = key
        output_file = f"{file_prefix}.html"
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError as e:
                print(f"Error deleting file {output_file}: {e}")
                continue  # Skip this iteration and move to the next key

        chapter = metadata['Chapter']
        title = metadata['title']
        page_number = key
        max_page_key = f'{len(front_matter):03d}'
        author_notes_html = markdown.markdown(metadata['note'], extensions=[Nl2BrExtension()])  # Convert the Markdown to HTML
        
        try:
            with open(output_file, 'w') as f:
                f.write('  <head>\n')
                f.write('    <meta charset="UTF-8">\n')
                f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
                f.write(f'    <title>{site_info["title"]} - By {site_info["author"]} - {title}</title>\n')
                f.write('    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" crossorigin="anonymous"></script>\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>\n')
                f.write('    <link href="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.css" rel="stylesheet" crossorigin="anonymous">\n')
                f.write('    <script src="https://cdnjs.cloudflare.com/ajax/libs/ekko-lightbox/5.3.0/ekko-lightbox.js" crossorigin="anonymous"></script>\n')
                f.write('    <link href="css/style.css" rel="stylesheet">\n')
                f.write('    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>\n')
                f.write('    <link rel="preconnect" href="https://fonts.googleapis.com/">\n')
                f.write('    <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">\n')
                f.write('</head>\n')              
                f.write('<div align="center">\n')

                # <header> section
                f.write('<div class="writeHeader">\n')
                f.write('<header align="center">\n')
                f.write('<a href="index.html"><img src="img/logo.png" alt=""></a>\n')
                f.write('<div id="nav">\n')
                f.write('</div>\n')
                f.write('</div>\n')
                
                # Add these lines to output Chapter, Page, and Title
                chapter = metadata['Chapter']
                page = metadata['page']
                f.write('<body>')
                f.write(f'<h1>Chapter: {chapter}</h1>\n')
                f.write(f'<h2>Page: {page}</h2>\n')
                f.write(f'<h2>Title: {title}</h2>\n')
                f.write('<div class="writeNav">\n')
                f.write(generate_navigation(page_number, max_page_key))
                f.write('</div>\n')
                f.write('<div class="comicPage">\n')

                matching_files = glob.glob(os.path.join(image_folder, f"{file_prefix}*.*"))
                for img_path in matching_files:
                    _, file_ext = os.path.splitext(img_path)
                    if file_ext == '.mp4':
                        f.write(f'<video src="{img_path}" controls>\n')
                        f.write(f'Your browser does not support the video tag.\n')
                        f.write(f'</video><br>\n')
                    else:
                        img_alt = metadata['desc']
                        f.write(f'<img src="{img_path}" alt="{img_alt}"><br>\n')

                f.write('</div>\n')

                f.write('<div class="writeNav">\n')
                f.write(generate_navigation(page_number, max_page_key))
                f.write('</div>\n')

                f.write('<h1>Author\'s Notes</h1>\n')
                # Add custom HTML if the current page has a matching key in custom_html_data
                if str(page_number) in custom_html_data:
                    f.write(custom_html_data[str(page_number)]['html'])

                f.write('<div class="authorNotes">\n')
                f.write(f'{author_notes_html}\n')
                f.write('</div>\n')
                f.write('</body>\n')


        except Exception as e:
            print(f"Error generating {output_file}: {e}")
            continue  # Skip this iteration and move to the next key

        print(f"Generated {output_file}")
        last_generated_file = output_file

    return last_generated_file


from_zone = tz.gettz('America/Los_Angeles')
to_zone = tz.gettz('UTC')

def generate_rss(front_matter, rss_file='rss.xml'):
    with open(rss_file, mode='w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<rss version="2.0">\n')
        f.write('    <channel>\n')
        f.write(f'        <title>{site_info["title"]} - By {site_info["author"]}</title>\n')
        f.write(f'        <link>{site_info["domain"]}</link>\n')
        f.write(f'        <description>{site_info["title"]}, a webcomic by {site_info["author"]}.</description>\n')
        f.write('        <language>en-us</language>\n')

        for key, metadata in sorted(front_matter.items(), reverse=True):
            file_prefix = key
            output_file = f"{file_prefix}.html"
            title = metadata['title']
            desc = metadata['desc']
            pub_date = datetime.strptime(metadata['date'], '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=from_zone).astimezone(to_zone).strftime('%a, %d %b %Y %H:%M:%S %z')

            f.write('        <item>\n')
            f.write(f'            <title>{title}</title>\n')
            f.write(f'            <link>{output_file}</link>\n')
            f.write(f'            <description>{desc}</description>\n')
            f.write(f'            <pubDate>{pub_date}</pubDate>\n')
            f.write('        </item>\n')

        f.write('    </channel>\n')
        f.write('</rss>\n')

    print(f"Generated {rss_file}")


def generate_archive(front_matter, site_info):
    try:
        with open('archive.html', 'w') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('  <head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">\n')
            f.write(f'    <title>{site_info["title"]} - By {site_info["author"]} - Archives</title>\n')
            f.write('    <link rel="stylesheet" href="css/style.css">\n')
            f.write('    <link href="https://fonts.googleapis.com/css?family=Mali&display=swap" rel="stylesheet">\n')
            f.write('  </head>\n')
            f.write('<body>\n')

            # <header> section
            f.write('<header>\n')
            f.write('  <div id="nav">\n')
            f.write('    <a href="index.html"><img src="img/logo.png" alt=""></a>\n')
            f.write('  </div>\n')
            f.write('</header>\n')

            f.write('<main>\n')
            f.write('  <section>\n')
            f.write('    <article>\n')
            f.write('      <div class="subPage archivePage">\n')
            f.write('        <table class="archiveTable">\n')

            # Table headers
            f.write('          <tr>\n')
            f.write('            <th>Chapter</th>\n')
            f.write('            <th>Title</th>\n')
            f.write('            <th>Description</th>\n')
            f.write('          </tr>\n')

            for key, metadata in sorted(front_matter.items()):
                file_prefix = key
                output_file = f"{file_prefix}.html"
                chapter = metadata['Chapter']
                title = metadata['title']
                desc = metadata['desc']

                f.write('          <tr>\n')
                f.write(f'            <td><a href="{output_file}">{chapter}</a></td>\n')
                f.write(f'            <td><a href="{output_file}">{title}</a></td>\n')
                f.write(f'            <td>{desc}</td>\n')
                f.write('          </tr>\n')

            f.write('        </table>\n')  # Close table
            f.write('      </div>\n')  # Close .subPage
            f.write('    </article>\n')
            f.write('  </section>\n')
            f.write('</main>\n')

            f.write('<script>\n')
            f.write('document.querySelectorAll(".archiveTable tr").forEach(row => {\n')
            f.write('  row.addEventListener("click", () => {\n')
            f.write('    const href = row.querySelector("a").getAttribute("href");\n')
            f.write('    window.location.href = href;\n')
            f.write('  });\n')
            f.write('});\n')
            f.write('</script>\n')
            f.write('</body>\n')
            f.write('</html>\n')


        print("Generated archive.html")
    except Exception as e:
        print(f"Error generating archive.html: {e}")
    
# Replace the navigation section in an HTML file
def replace_nav_in_html(html_file, new_nav_html):
    try:
        with open(html_file, 'r+') as f:
            soup = BeautifulSoup(f, 'html.parser')
            nav_div = soup.find('div', {'id': 'nav'})
            if nav_div:
                nav_div.replace_with(BeautifulSoup(new_nav_html, 'html.parser'))
            else:
                print(f"No 'div' with id 'nav' found in {html_file}. Skipping...")
                return
            # Write the modified HTML back to the file
            f.seek(0)
            f.write(str(soup))
            f.truncate()
        print(f"Replaced navigation in {html_file}")
    except Exception as e:
        print(f"Error processing {html_file}: {e}")

site_info = read_site_info("site_info.yaml")

if __name__ == "__main__":
    front_matter = read_yaml_file("front_matter.yaml")
    last_generated_file = generate_html(front_matter, site_info)
    # Print the last generated file
    print(f"Last generated file: {last_generated_file}")

    # Create a copy of the last generated HTML file as index.html
    try:
        shutil.copy(last_generated_file, "index.html")
        print("Created index.html")
    except shutil.Error as e:
        print(f"Error creating index.html: {e}")

    # Generate RSS feed
    generate_rss(front_matter)

    # Generate archive
    generate_archive(front_matter, site_info)

    # Update navigation in HTML files
    nav_yaml_file = 'header.yaml'
    nav_yaml_data = read_header_links(nav_yaml_file)
    new_nav_html = generate_navigation_yaml(nav_yaml_data)

    html_files = glob.glob("*.html")
    for html_file in html_files:
        replace_nav_in_html(html_file, new_nav_html)