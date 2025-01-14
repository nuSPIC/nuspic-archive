import re
import shutil
from pathlib import Path

SOURCE_DIR = Path('mirror/nuspic.g-node.org')
TARGET_DIR = Path('cleaned')

REPLACEMENTS = {
    r"""static/images/exernal/neurofilament_egert_small.html""": r"static/images/external/neurofilament_egert_small.jpg",
    r"""'/static/images/""": r"'static/images/",

    r"""<link rel="alternate" type="application/atom\+xml" title="Latest news" href="([./]+)?feed/news/index.html" />""": r"",
    r"""<a href="([./]+)?feed/news/index.html">Latest news</a>""": r"Latest news",

    r"""
    \s+<li class="" title="Tutorials"><a href="#">
    \s+<i class="fa fa-graduation-cap"></i> <span class="hidden-md hidden-sm">Tutorials</span></a></li>""": r"",

    r"""\
    \s+<li class="" title="Community"><a href="([./]+)?accounts/index.html">
    \s+<i class="fa fa-users"></i> <span class="hidden-md hidden-sm">Community</span></a></li>""": r"",

    r"""\
    \s+<li class="" title="Discussions"><a href="([./]+)?forum/index.html">
    \s+<span class="glyphicon glyphicon-tree-deciduous"></span> <span class="hidden-md hidden-sm">Discussions</span></a></li>""": r"",

    r"""href="\d/\d/index.html" """: """href="#" """,

    r"""<a href="forum/index.html">([\S ]+)</a>""": r"\1",

    r"""
                    <ul class="nav navbar-nav navbar-right">
\s+   
                        <li class="">
                            <a href="([./]+)?accounts/login/index.html">
                                <i class="fa fa-sign-in"></i> Login
                            </a>
                        </li>
                        <li class="">
                            <a href="([./]+)?accounts/registration/index.html">
                                <i class="fa fa-edit"></i> Register
                            </a>
                        </li>
\s+
                    </ul>""": r"",

    r"""
    <script type="text/javascript">

      var _gaq = _gaq \|\| \[\];
      _gaq.push\(\['_setAccount', 'UA-3087437-3']\);
      _gaq.push\(\['_trackPageview']\);

      \(function\(\) {.+}\)\(\);

    </script>""": r"",

    r"http://": r"https://",

    r"../www\.g-node\.org/index\.html": r"https://www.g-node.org",
    r"nuspic_poster\.html": r"nuspic_poster.pdf",

    r"""(<div style="margin : 20px 0 ;">)""": r"""\1<hr>
    <div class="text-danger">
    <strong>Update as of January, 2025</strong>: After more than a decade of active service, it's time to retire the 
    original nuSPIC public server. Software outdated by more than a decade makes it impractical to continue running a 
    public service. However, we are happy to announce that an actively maintained successor project, 
    <a href="https://nest-desktop.github.io">NEST Desktop</a>, is ready to fill the gap and provide an even better 
    <a href="https://nest-desktop.readthedocs.io/en/latest/about/nuspic.html">nuSPIC experience</a> for new generations
    of researchers! This static website and all code related to nuSPIC will remain archived on the 
    <a href="https://github.com/nuSPIC">nuSPIC GitHub organization</a>. We thank all contributors and users over the 
    years and wish them continued success in scientific discovery!    
    </div>
    """
}

shutil.rmtree(TARGET_DIR, ignore_errors=True)

shutil.copytree(SOURCE_DIR / "static", TARGET_DIR / "static")
shutil.copytree(SOURCE_DIR / "media", TARGET_DIR / "media")

for file in SOURCE_DIR.glob('**/*.html'):
    content = file.read_text()

    for search, replace in REPLACEMENTS.items():
        content = re.sub(search, replace, content, flags=re.DOTALL)

    output_dir = Path(str(file.parent).replace(str(SOURCE_DIR), str(TARGET_DIR)))
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / file.name).write_text(content)

shutil.rmtree(TARGET_DIR / "accounts", ignore_errors=True)
shutil.rmtree(TARGET_DIR / "feed", ignore_errors=True)
shutil.rmtree(TARGET_DIR / "forum", ignore_errors=True)

for subdir in TARGET_DIR.glob("network/*"):
    if subdir.is_dir():
        shutil.rmtree(subdir, ignore_errors=True)

shutil.rmtree(TARGET_DIR / "static" / "images" / "exernal", ignore_errors=True)
