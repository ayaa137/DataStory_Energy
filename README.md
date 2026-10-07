# Visual Communication and Data Story Telling Playground

This is a template repository. You can make your own repos based on this template. 

## Get your playground ready

1. Create your own playground repository from this template (Green Button top right). Give it a name like `VisComPlayground`. 
2. Clone your repository to your computer. (Open Folder from Git)
3. In TERMINAL: Type `quarto render` to produce the website. 
4. Open the website in your browser by clicking on `_site/index.html`
5. Explore the different HTML-page types in the HTML but also in their source type:
    - A **report** in a typical article style with references, numbered figures, and crossreferences. 
    - More **referencing** in the "Bibliograpy Example"
    - A **slide deck** in the "Presentation"
    - An example of **"Data Scrollytelling"** 
6. The scripts `CountryBubbles.R` and `WarmingStripes.R` are files with code for producing Visuals. Make your own visuals, and develop a sense for what is needed for a great visual in a data story. 

## Make your DataStory repo from here

The default delivery in **Visual Communication and Data Storytelling** is a repository with the 

- The **slide deck** of your data story in *narrative* form (Default reproducible format: Quarto Revealjs HTML)
- The accompanying **report** of your data story in *news article* form (Default reproducible format: Quarto HTML)

Alternatively, a narrative scrollytelling part can replace the slide deck (Format: Quarto closeread-html)   
Additionally a dashboard with interactive graphics for self exploration of readers


### Step-by-step guide: How to make a minimal version from your DataStory


1. On GitHub: Create another repository from this template (Green Button top right). Name it `DataStory_KEYWORD`. Replace KEYWORD with one keyword describing your data story. 
2. On GitHub: Add all team members as collaborators. Settings -> Collaborators -> Add people -> *Type in GitHub-name to add*
    - If you chose to keep your repository private, you need to add the instructor as a collaborator for assessment! 
4. On your computers: Clone the repository to your computer. (Open Folder from Git)
5. On your computer: Remove 
    - `bibliography-example.qmd`
    - `CountryBubbles.R`
    - `WarmingStripes.R`
    - `scrollytelling.qmd`
    - all files in `data/`
6. Update in `_quarto.yml`: In `website:navbar:left:` remove the lines `bibliography-example.qmd` and `scrollytelling.qmd`. Enter the title of your Data Story 
7. On bibliography: When you export your own bibliography file from Zotero save it in the same place as `Visual Communication and Data Storytelling.json`. Then go to `index.html` and replace the filename in the YAML `bibliography:`. Then you can delete the old `.json` file. 
8. On `_extensions`: If you do not do a scrollytelling part you can delete this folder. 
9. `quarto render` in TERMINAL to test if it works. 
10. Remove this very text from `README.md` (this very file) and write some short basic info about what your repo is. 
11. Source Control Pane: Commit all changes (including the deleted files), and push to GitHub

Now you have a simplified file structure for your Data Story. Start editing:

- `index.qmd` with the basic structure of about your report, like title and authors. Remove all the text and put a draft for your structure. 
- `presentation.qmd` with title and a first structure of `## HEADLINES` to specifiy some slides you want to have
- Put your data in the data folder.