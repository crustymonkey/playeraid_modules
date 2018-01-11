# Playeraid.net modules
If you enjoy the handy player aids found on https://playeraid.net and you'd like to contribute, these are some basic instructions to get you started.

**IMPORTANT: This is currently an alpha level implementation.  Many features will likely be added in the future, and some things in this document will change.**

# Necessary Skills
There are a few things you will need to know to get started.

* The best/easiest/highly recommended way to submit your contributions is through github here.  If you've used it at all, there is workflow of: fork a repository, make edits, submit a pull request.  This is the easiest for me to process/test.  However, if github is a little intimidating, you can just zip up your directory and email a Dropbox (or similar) link to it for me (admin@splitstreams.com) to get it from you.  **Please don't send it as an attachment**
* You will need to understand the basic concepts of construction of a YAML file, specifically [PyYAML](http://pyyaml.org/wiki/PyYAML).  There are many tutorials on the internet covering YAML, but [this one](https://learn.getgrav.org/advanced/yaml) covers the very basics. It also has some other helpful links at the bottom of the page.  Alternatively, you can use JSON instead of YAML, but it's a little more finicky to use and make valid.
* You will either need to know some basic HTML, or [Markdown](https://daringfireball.net/projects/markdown/syntax).  Markdown is recommended for simplicity.  
    * If you are using HTML, you will want to use basic tags like `<p>` tags, `<b>` tags, `<i>` tags, and maybe list (`<ol>` and `<ul>`).  You are only using these tags for some basic output formatting.  You don't have to be any kind of html expert here.
    * If you are using Markdown, I would highly recommend using the **Photosynthesis** player aid as an example.  Note the use of `text: |` syntax for the multiline text blocks.  This is important for markdown as the `|` will preserve your whitespace properly.

The best advice here is just to look through some of the existing player aids and you should be able to figure out what you need to do.

# Standards and Rules
There are some things you will have to adhere to for your submissions to be used.  They are pretty simple rules, and mostly obvious.

* Your YAML/JSON **must be valid**.  There are validators out there that will test these files for validity before submission.  I will test them myself upon submission, but I would ask you make sure they are syntactically valid before submitting.  You can also test them on the playeraid site.  See Testing Your Module below.
* Your YAML/JSON should be easily human readable.  This means you need to use indentation for sub-sections and things should line up.  If you submit an unindented mess, it will be rejected.
* If you choose to use HTML, your html snippets must be well formed.  This basically means that you have to close your tags.  So, for example, a `<p>` tag needs to have its closing `</p>` tag.  Your submission will be rejected if it is not well formed.
* `<script>` tags are forbidden.  You cannot run any javascript from within your playeraids.  There should never be a case where this is necessary.
* I use an 80 character line limit for my files, **you do not have to**.  I will not enforce this on anyone else. But, again, it should be properly indented and readable.
* Your directories/files may only contain the following characters: "a" to "z" and underscore.  Though multiple languages are supported in the data files themselves, the directories and files must follow this rule.

# Directory Layout
Your directory should be layed out as follows:

```
- <The top level directory should be named for the game> example: amun_re
  - <language 1>  <- This should be named for the 2 letter language code ("en")
    - playeraid.yaml -or- playeraid.json
  - <language 2>
  - <language N>
  - img <- This is a directory that you can put images in.  You can use these images in your aids.  More on images below.
```


# Data Layout
The layout of your data in your YAML/JSON file is pretty simple.  The allowed key values in the mappings are pretty straightforward here.

## The Top Level of the Data Structure
This will have the following 5 mapping items:

* **name** (required): This is the name that will show up on the playeraid.net home page
* **description** (required):  This is a short description of the game.  This could just be a simple link to the BGG page
* **credits** (optional):  If you are copying this playeraid from an existing aid and wish to credit the original creator, you can specify them here.  You can also add your own name if you put this aid together.
* **sections** (required): This will map to a list of your sections (more on `sections` below).
* **enabled** (optional): This is either *true* or *false* for whether it is enabled.  You must set this to *true* to enable your player aid.  The default is *false*
* **text_type** (optional): This is either *html* or *markdown*. If not specified, the default is *html*.

## Sections
This is the meat of your player aid.  Each section will have up to 3 items in it, including another `sections` mapping.  This means you can have nested sections within sections.  You can find examples of these on https://playeraid.net.

These are the 3 items that can appear in a section:

* **name** (required): This will appear as the heading for the section.  This is the clickable portion that will open up and reveal any text or sections below it.
* **text** (optional): This is text that will appear directly under your section.  This will contain any html snippets to format what appears in this section.
* **sections** (optional): In addition, or in lieu of, a `text` section, you can have another `sections` item to nest more sections.  You can nest as deeply as is reasonable.

# Images
In the `img` directory, you can add images that are referenced in your playeraid in an `<img>` tag.  All images sources will be prepended with this path: `/static/img/<name of module directory/`.

**Example:** If your module is for Amun Re, and your directory is `amun_re`, then you have an image in the `img` directory, and that image is named `image1.jpg`, you would add the following html tag to your playeraid file to show that image:

```
<img src="/static/img/amun_re/image1.jpg" width="30" height="30" />
```

(Note that you can optionally specify a width and height for the image there)

**For Markdown**: You can also specify images, using the same path building as above.  The markdown syntax is as follows (using the same path as above):

```
![alt text](/static/img/amun_re/image1.jpg)
```

# Testing Your Module
You can test your module by entering the text here: https://playeraid.net/test

Note that this is primarily for testing the layout.

## Things To Note About Testing
* Images will not work.  They will appear broken
* If you are using HTML, your HTML code will **not** be rendered.  This is to prevent exploits on the site.  You'll be able to see what your layout looks like, and it will show you the escaped HTML.  It's pretty easy to test HTML locally using a `file://` url.
* If you are using Markdown, everything in the aid **will** be rendered.

# Future Plans
I plan on adding in some other features to this at some point.  I'm thinking that I may allow an optional css file for more individualized styling.  I'm also open to suggestions if people have ideas for improving this.
