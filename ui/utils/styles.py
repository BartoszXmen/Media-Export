def build_styles(accent):

    return f"""
#app {{
    background:#121212;
}}

QMainWindow {{
    background:transparent;
}}

#panel {{
    background:rgba(28,28,28,0.92);
    border-radius:16px;
    padding:20px;
}}

#title {{
    color:white;
}}

#author {{
    color:#e6e6e6;
}}

#authorCard {{
    background:rgba(35,35,35,0.95);
    border-radius:14px;

    border:1px solid rgba(255,255,255,0.06);
}}

#authorCard:hover {{
    border:1px solid rgba(255,255,255,0.12);
}}

QProgressBar {{
    background:#1e1e1e;
    border-radius:6px;
    height:10px;
}}

QProgressBar::chunk {{
    border-radius:6px;
    background:{accent};
}}

QPushButton {{
    background:{accent};
    border-radius:8px;
    padding:8px;
}}

#folderBtn {{
    background: rgb(255, 232, 150);
    border-radius: 6px;
    border: none;
}}

#folderBtn:hover {{
    background: rgb(255, 224, 120);
}}

#folderBtn:pressed {{
   background: rgb(255, 210, 90);
}}

QPushButton:hover {{
    background:rgba(255,255,255,0.15);
}}


"""