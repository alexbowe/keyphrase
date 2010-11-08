"""
The master build SConstruct file. This pulls in everything else and makes
things happen.
"""

import os
import sys
import build_config

# Make a new environment.
env = Environment(ENV=os.environ, tools = ['default'])

# Get all the nested SConscripts in that may alter and pass back
# the environment.
env = SConscript('aux/SConscript', 'env')

class LatexBuilder(object):
    """To facilitate the build of "complex" LaTeX documents."""

    def __init__(self, latex_project):
        """Constructor. Takes the LaTeX main file as input."""
        self.latex_project = latex_project
        self.markdown = []
        self.to_clean = []
        self.chapters = []
        self.chapter_configs = {}
        self.figures = {}
        self.pdf_output = None
        self.dvi_output = None
        self.makeindex_file_list = [self.latex_project + x
                                    for x in build_config.MAKEINDEX_EXTENSIONS]
        
        self.figures = {'eps': [],
                        'pdf': [],
                        'png': [],
                        'jpg': [],
                        'graffle': [],
                        'gnuplot': []}
        
        self._get_markdown()
        self._build_markdown()
        self._get_chapters()
        self._get_chapter_configs()
        #self._collect_figures_from_configs()
        self._collect_figures_from_dirs()        
    
    def _get_markdown(self):
        """Finds preliminary Markdown files."""
        markdown_files = os.path.join(build_config.CHAPTER_DIRECTORY,
                                      '*.md')
                                                                   
        self.markdown = [os.path.split(x)[-1][:-3]
                         for x in Glob(markdown_files, strings=True)]
        print self.markdown
    
    def _build_markdown(self):
        """Builds preliminary Markdown files."""
        # should somehow work out dependencies eventually...
        # but the markdown files need to be compiled to get the .tex files
        # as SCons reads this SConstruct...
        to_clean = []
        for item in self.markdown:
            md_file = os.path.join(build_config.CHAPTER_DIRECTORY, item +
                build_config.FILE_EXTENSIONS['md'])
            tex_file = os.path.join(build_config.CHAPTER_DIRECTORY,
                item + build_config.FILE_EXTENSIONS['tex'])
            self.to_clean.append(tex_file)
            
            os.system('pandoc ' + md_file + ' -o ' + tex_file)
    
    def _get_chapters(self):
        """Collect chapter names."""
        chapter_finder = os.path.join(build_config.CHAPTER_DIRECTORY,
                                      '*.tex')
        self.chapters = [os.path.split(x)[-1][:-4]
                         for x in Glob(chapter_finder, strings=True)]
    
    
    def _get_chapter_configs(self):
        """Load the chapter config modules."""
        import_list = ['%s_config' % x for x in self.chapters]
        chapter_modules = __import__(build_config.CHAPTER_DIRECTORY,
                                     globals(), locals(),
                                     import_list)
        self.chapter_configs = {}
        for item in dir(chapter_modules):
            if item.endswith('_config'):
                self.chapter_configs[item[:-7]] = getattr(chapter_modules, item)
    
    
    def build_config(self):
        """Configure the two build targets for DVI and PDF output."""
        self.dvi_output = env.DVI(source=self.latex_project + '.tex',
                                 target=self.latex_project + '.dvi')
        env.Alias('dvi', self.latex_project + '.dvi')
        Clean(self.dvi_output, self.makeindex_file_list + self.to_clean)
        
        self.pdf_output = env.PDF(source=self.latex_project + '.tex',
                                  target=self.latex_project + '.pdf')
        env.Alias('pdf', self.latex_project + '.pdf')
        env.Clean(self.pdf_output, self.makeindex_file_list + self.to_clean)
        
        env.Default(build_config.DEFAULT_TARGET)
    

    def _collect_figures_from_configs(self):
        """Find all figures in the modules and add them to my list."""
        for chapter in self.chapter_configs.keys():
            module = self.chapter_configs[chapter]
            self.figures['eps'].extend([os.path.join(chapter, x)
                                        for x in Split(module.EPS_FIGURES)])
            self.figures['pdf'].extend([os.path.join(chapter, x)
                                        for x in Split(module.PDF_FIGURES)])
            self.figures['png'].extend([os.path.join(chapter, x)
                                        for x in Split(module.PNG_FIGURES)])
            self.figures['jpg'].extend([os.path.join(chapter, x)
                                        for x in Split(module.JPG_FIGURES)])
            self.figures['gnuplot'].extend([os.path.join(chapter, x)
                                        for x in Split(module.GNUPLOT_FIGURES)])
            self.figures['graffle'].extend([os.path.join(chapter, x)
                                        for x in Split(module.GRAFFLE_FIGURES)])


    def _find_files(self, chapter, extension):
        """Find all files with a certain extension for a given chapter."""
        find_pattern = os.path.join(build_config.IMAGES_DIRECTORY,
                                    chapter, '*%s' % extension)
        found_files = Glob(find_pattern, strings=True)
        # Strip off the extensions.
        length_extension = len(extension)
        found_files = [x[x.index(os.sep) + 1:-length_extension]
                       for x in found_files]
        return found_files
    
    
    def _collect_figures_from_dirs(self):
        """Find all figures in the modules and add them to my list."""
        for chapter in self.chapters:
            for extension in ['eps', 'pdf', 'png', 'jpg', 'gnuplot', 'graffle']:
                new_files = self._find_files(chapter,
                                             build_config.FILE_EXTENSIONS[extension])
                self.figures[extension].extend(new_files)


    def _build_gnuplot(self, gnuplot_figures):
        """Build GNUplot figures."""
        for item in gnuplot_figures:
            gnuplot_file = os.path.join(build_config.IMAGES_DIRECTORY,
                                        item + build_config.FILE_EXTENSIONS['gnuplot'])
            eps_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            pdf_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['pdf'])
            env.Gnuplot(source=gnuplot_file, target=eps_file)
            dep = env.Eps2pdf(source=eps_file, target=pdf_file)
            env.Depends(dep, eps_file)
            env.Depends(self.dvi_output, eps_file)
            env.Depends(self.pdf_output, pdf_file)
    
    def _build_graffle(self, graffle_figures):
        """Build Omnigraffle Figures"""
        for item in graffle_figures:
            graffle_file = os.path.join(build_config.IMAGES_DIRECTORY, item +
                                        build_config.FILE_EXTENSIONS['graffle'])
            eps_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            pdf_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['pdf'])
            env.Graffle(source=graffle_file, target=eps_file)
            dep = env.Eps2pdf(source=eps_file, target=pdf_file)
            env.Depends(dep, eps_file)
            env.Depends(self.dvi_output, eps_file)
            env.Depends(self.pdf_output, pdf_file)


    def _build_png(self, png_figures):
        """Build PNG2EPS targets."""
        for item in png_figures:
            png_file = os.path.join(build_config.IMAGES_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['png'])
            eps_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            env.Png2eps(eps_file, png_file)
            env.Depends(self.dvi_output, eps_file)


    def _build_jpg(self, jpg_figures):
        """Build JPG2EPS targets."""
        for item in jpg_figures:
            jpg_file = os.path.join(build_config.IMAGES_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['jpg'])
            eps_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            env.Jpg2eps(eps_file, jpg_file)
            env.Depends(self.dvi_output, eps_file)


    def _build_pdf(self, pdf_figures):
        """Build PDF2EPS targets."""
        for item in pdf_figures:
            eps_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            pdf_file = os.path.join(build_config.IMAGES_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['pdf'])
            env.Pdf2eps(eps_file, pdf_file)
            env.Depends(self.dvi_output, eps_file)


    def _build_eps(self, eps_figures):
        """Build EPS2PDF targets."""
        for item in eps_figures:
            eps_file = os.path.join(build_config.IMAGES_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['eps'])
            pdf_file = os.path.join(build_config.GENERATED_DIRECTORY,
                                    item + build_config.FILE_EXTENSIONS['pdf'])
            env.Eps2pdf(pdf_file, eps_file)
            env.Depends(self.pdf_output, pdf_file)


    def build_figures(self):
        """Build all figures according to dependencies."""
        self._build_gnuplot(self.figures['gnuplot'])
        self._build_graffle(self.figures['graffle'])
        self._build_png(self.figures['png'])
        self._build_jpg(self.figures['jpg'])
        self._build_pdf(self.figures['pdf'])
        self._build_eps(self.figures['eps'])


def main():
    """Do the magic of building the LaTeX document."""
    # Set the number of maximum LaTeX retries to 4, as we need it here.
    env['LATEXRETRIES'] = 4
    builder = LatexBuilder(build_config.LATEX_PROJECT)
    builder.build_config()
    builder.build_figures()


# Make it so!
main()
