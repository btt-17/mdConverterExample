import markdown

def preprocess(text):
    lines = text.split("\n")
    new_lines = []

    output = []

    content = []
    startCodeBlock = False

        
    for i in range(len(lines)):
        if "```" in lines[i]:
            if startCodeBlock == True:
                # print(content)
                new_lines.append(content)
                content = []
                startCodeBlock = False
            else:
                startCodeBlock = True 
                content.append(lines[i])
        else:
            if startCodeBlock:
                content.append(lines[i])
            else:
                new_lines.append(lines[i])
        

    for i in range(len(new_lines)):
        # print(new_lines[i])
        if new_lines[i] != "---":
            content.append(new_lines[i])
        else:
            output.append(content)
            content = []

    if len(content) > 0:
        output.append(content)
    print(output)
    return output


def convert_to_html(markdown_text):

# print(output)

    html = """
    <!DOCTYPE html>
    <html>\n
    """
    ### 
    add_script_for_slideshow = """
    <script>
    let slideIndex = 1;
    showSlides(slideIndex);

    function plusSlides(n) {
    showSlides(slideIndex += n);
    }

    function currentSlide(n) {
    showSlides(slideIndex = n);
    }

    function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    
    if (n > slides.length) {slideIndex = 1}    
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }

    slides[slideIndex-1].style.display = "block";  
    
    }
    </script>
    \n
    """

    #### Header

    head_html = "<head>\n" \
    + """
    <meta name="viewport" content="width=device-width, initial-scale=1">\n
    """ \
    + """
    <style>
    * {box-sizing: border-box}
    body {font-family: Verdana, sans-serif; margin:0}


    .slideshow-container {
        padding-top: 20vh;
        padding-left: 10vh;
    }

    .codeBlock { 
        background-color: black;
        color: white;
        max-width: 30vw;
        margin-left: 30vw;
        padding-left: 5px;
    }

    .slideshow-container * {
        font-size: 22px;
        margin-top: 12px;
    }

    .slider { 
      text-align: center;
      font-size: 90px;;
    }
    </style>\n
    """  +"\n</head>\n"


    ## body

    body_html = "<body>\n"

    body_html += '<div class="slideshow-container">\n'

    for i in range(len(markdown_text)):
        slide_div = f"""
            <div class="mySlides fade">
                <div class="numbertext">{i+1} / 3</div>
            \n
        """
        for s in markdown_text[i]:
            if isinstance(s, str):
                line_html = markdown.markdown(s)
                slide_div += line_html + "\n"
            else:
                print(s)
                code_block = s 
                code_block_html = """
                <div class="codeBlock">\n
                """
                for el in code_block:
                    code_block_html +="<div>" + el + "</div>"+ "\n"
                code_block_html += "</div>"
                slide_div += code_block_html + "\n"



        slide_div += "</div>\n"
        body_html += slide_div
    
    body_html += """
    <div class="slider">
        <a class="prev" onclick="plusSlides(-1)">❮</a>
        <a class="next" onclick="plusSlides(1)">❯</a>
    </div>
    \n
    """
    body_html += "</div>\n"
    body_html += add_script_for_slideshow
    body_html += "</body>\n"

    html += head_html + body_html + "\n</html>\n"
    return html

    



if __name__=="__main__":
    text = """
# **Example**

 Presentation Example



---

# How to write slides

Split pages by horizontal ruler (`---`). It's very simple! :satisfied:

```markdown
# Slide 1

foobar

---

# Slide 2

foobar
```

---

# New example (duplicate)



```markdown
# Slide 3

foobar

---

# Slide 4

foobar
```
"""
    markdown_text = preprocess(text)
    html = convert_to_html(markdown_text)
    with open("test.html", "w") as fp:
        fp.write(html)
        fp.close()