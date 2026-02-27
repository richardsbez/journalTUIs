<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>todoTerminal</title>
</head>
<body>

  <h1>📓 toDoTerminal</h1>

  <p>
    <strong>A powerful terminal-based task, goal, and habit manager — lightweight, fast, and dependency-free.</strong><br/>
    Designed for developers and productivity enthusiasts who prefer the keyboard over the mouse.
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" />
    <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" />
    <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square" />
  </p>


<!-- Screenshots Pyramid Layout -->

<div style="margin: 60px 0; text-align: center;">
  <h2 style="margin-bottom: 40px;">📸 Screenshots</h2>
  <!-- Top row -->
  <div style="
      display: flex;
      justify-content: center;
      gap: 30px;
  ">
    <img 
      src="https://github.com/user-attachments/assets/0a930644-c92b-406f-a01f-c15f781e4110"
      alt="Dashboard View"
      style="
        width: 420px;
        max-width: 45%;
        border-radius: 14px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25);
      "
    />
    <img 
      src="https://github.com/user-attachments/assets/96619081-3586-4a9e-9a3c-b13eb0535281"
      alt="Goals View"
      style="
        width: 420px;
        max-width: 45%;
        border-radius: 14px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.25);
      "
    />
  </div>
  <!-- Bottom row -->
  <div style="
      display: flex;
      justify-content: center;
      margin-top: 40px;
  ">
    <img 
      src="https://github.com/user-attachments/assets/f7b8270a-efaa-468c-929b-878e58e1dde7"
      alt="Statistics View"
      style="
        width: 520px;
        max-width: 60%;
        border-radius: 16px;
        box-shadow: 0 18px 40px rgba(0,0,0,0.35);
      "
    />
  </div>
</div>


  <hr/>

  <h2> Features</h2>

  <ul>
    <li><strong> Notebooks</strong> — Organize tasks into separate contexts (Today, College, Work, Personal…)</li>
    <li><strong> Tasks</strong> — Create, edit, complete, reopen, delete and prioritize with color-coded indicators</li>
    <li><strong> Goals</strong> — Track weekly, monthly and yearly progress with visual progress bars</li>
    <li><strong> Calendar</strong> — Mark days as complete, partial or pending</li>
    <li><strong> Heatmap</strong> — Visualize habit consistency for the current week</li>
    <li><strong> Quick Notes</strong> — Free-text notes per notebook</li>
    <li><strong> Statistics</strong> — Productivity overview by notebook and category</li>
    <li><strong> Auto-Save</strong> — Data persisted locally in JSON (no database required)</li>
  </ul>

  <hr/>

  <h2> Installation</h2>

  <pre><code>
# Clone the repository
git clone https://github.com/your-username/todoTerminal.git
cd todoTerminal

# Run directly (no installation needed)
python main.py
  </code></pre>

  <p><strong>Requirements:</strong> Python 3.10+ (No external libraries required)</p>

  <hr/>

  <h2>📁 Project Structure</h2>

  <pre><code>
todoTerminal/
│
├── main.py                  # Entry point — control loop
│
├── core/                    # Application core (no UI dependencies)
│   ├── colors.py            # ANSI color constants
│   ├── constants.py         # Global settings and constants
│   └── storage.py           # Data persistence (JSON)
│
├── ui/                      # Interface layer
│   ├── utils.py             # Reusable helpers (bars, feedback, etc.)
│   ├── dashboard.py         # Main screen: tasks + goals + heatmap
│   └── notebooks.py         # Notebook selection screen
│
└── features/                # Standalone features
    ├── tasks.py             # Task and notebook CRUD
    ├── goals.py             # Weekly / monthly / yearly goals + calendar
    ├── heatmap.py           # Daily activity tracking
    ├── notes.py             # Quick notes per notebook
    └── stats.py             # Productivity statistics
  </code></pre>

  <hr/>

  <h2>⌨️ Commands</h2>

  <h3>Main Screen</h3>

  <table border="1" cellpadding="8" cellspacing="0">
    <thead>
      <tr>
        <th>Key</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>+</strong></td><td>Add task</td></tr>
      <tr><td><strong>X</strong></td><td>Complete / Reopen task</td></tr>
      <tr><td><strong>E</strong></td><td>Edit task text</td></tr>
      <tr><td><strong>D</strong></td><td>Delete task</td></tr>
      <tr><td><strong>P</strong></td><td>Change priority</td></tr>
      <tr><td><strong>M</strong></td><td>Manage goals</td></tr>
      <tr><td><strong>A</strong></td><td>Quick notes</td></tr>
      <tr><td><strong>H</strong></td><td>Log activity (heatmap)</td></tr>
      <tr><td><strong>S</strong></td><td>General statistics</td></tr>
      <tr><td><strong>C</strong></td><td>Notebook menu</td></tr>
      <tr><td><strong>Q</strong></td><td>Quit</td></tr>
    </tbody>
  </table>

  <h3>Priority Levels</h3>

  <table border="1" cellpadding="8" cellspacing="0">
    <thead>
      <tr>
        <th>Symbol</th>
        <th>Level</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>🔴</td><td>1 — High</td></tr>
      <tr><td>🟡</td><td>2 — Medium</td></tr>
      <tr><td>🟢</td><td>3 — Low</td></tr>
    </tbody>
  </table>

  <hr/>

  <h2> Data Persistence</h2>

  <p>
    All data is automatically saved to <code>journal_data.json</code> in the execution directory.
  </p>

  <p>
    To back up your data, simply copy this file.
  </p>

  <p>
    <code>journal_data.json</code> is included in <code>.gitignore</code> by default —
    your personal data will never be pushed to the repository.
  </p>

  <hr/>

  <h2> Development</h2>

  <h3>VS Code Setup</h3>

  <p>
    The project includes <code>pyrightconfig.json</code> to resolve Pylance import warnings.
    If errors persist after cloning:
  </p>

  <ol>
    <li>Press <strong>Ctrl + Shift + P</strong></li>
    <li>Select <strong>"Python: Select Interpreter"</strong></li>
    <li>Choose your Python 3.10+</li>
    <li>Press <strong>Ctrl + Shift + P</strong> again</li>
    <li>Select <strong>"Reload Window"</strong></li>
  </ol>

  <h3>Adding a New Feature</h3>

  <ol>
    <li>Create <code>features/your_feature.py</code></li>
    <li>Implement the main function receiving <code>data: dict</code></li>
    <li>Import and register the command in the <code>COMMANDS</code> dictionary inside <code>main.py</code></li>
  </ol>

  <hr/>

  <h2>📜 License</h2>

  <p>
    This project is licensed under the MIT License.
  </p>

  <hr/>

  <p align="center">
    Built for terminal lovers ⚡
  </p>

</body>
</html>
