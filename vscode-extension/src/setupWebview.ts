import * as vscode from 'vscode';
import { getPreferences, persistPreferences, IdentityPreferences } from './config';

export class SetupWebviewPanel {
  public static currentPanel: SetupWebviewPanel | undefined;
  private readonly _panel: vscode.WebviewPanel;
  private readonly _extensionUri: vscode.Uri;
  private _disposables: vscode.Disposable[] = [];

  public static render(extensionUri: vscode.Uri) {
    if (SetupWebviewPanel.currentPanel) {
      SetupWebviewPanel.currentPanel._panel.reveal(vscode.ViewColumn.One);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'identitySetup',
      'Identity Generator: Setup & Preferences',
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        retainContextWhenHidden: true,
      }
    );

    SetupWebviewPanel.currentPanel = new SetupWebviewPanel(panel, extensionUri);
  }

  private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
    this._panel = panel;
    this._extensionUri = extensionUri;

    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    this._panel.webview.html = this._getHtmlForWebview();

    this._panel.webview.onDidReceiveMessage(
      async (message) => {
        switch (message.command) {
          case 'browseFolder':
            const uris = await vscode.window.showOpenDialog({
              canSelectFiles: false,
              canSelectFolders: true,
              canSelectMany: false,
              openLabel: 'Select Storage Folder',
            });
            if (uris && uris.length > 0) {
              this._panel.webview.postMessage({
                command: 'setFolder',
                path: uris[0].fsPath,
              });
            }
            return;

          case 'savePreferences':
            const updatedPrefs: IdentityPreferences = {
              defaultLocation: message.data.defaultLocation,
              defaultFields: message.data.defaultFields,
              defaultQuantity: parseInt(message.data.defaultQuantity, 10) || 1,
              defaultFormat: message.data.defaultFormat,
              folderName: message.data.folderName || 'generated-names',
              setupCompleted: true,
            };
            await persistPreferences(updatedPrefs);
            vscode.window.showInformationMessage(
              'Identity Generator preferences saved successfully! You can now run "identity generate" in the integrated terminal.'
            );
            this.dispose();
            return;
        }
      },
      null,
      this._disposables
    );
  }

  public dispose() {
    SetupWebviewPanel.currentPanel = undefined;
    this._panel.dispose();
    while (this._disposables.length) {
      const x = this._disposables.pop();
      if (x) {
        x.dispose();
      }
    }
  }

  private _getHtmlForWebview(): string {
    const prefs = getPreferences();
    const hasName = prefs.defaultFields.includes('name');
    const hasEmail = prefs.defaultFields.includes('email');
    const hasPass = prefs.defaultFields.includes('password');
    const hasPhone = prefs.defaultFields.includes('phone');

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Identity Generator Setup</title>
  <style>
    body {
      font-family: var(--vscode-font-family, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif);
      color: var(--vscode-foreground);
      background-color: var(--vscode-editor-background);
      padding: 24px 32px;
      line-height: 1.5;
      max-width: 680px;
      margin: 0 auto;
    }
    h2 {
      font-size: 1.5rem;
      margin-bottom: 4px;
      color: var(--vscode-editor-foreground);
    }
    .subtitle {
      color: var(--vscode-descriptionForeground);
      margin-bottom: 24px;
      font-size: 0.95rem;
    }
    .section {
      background: var(--vscode-editorWidget-background, rgba(127, 127, 127, 0.08));
      border: 1px solid var(--vscode-widget-border, rgba(127, 127, 127, 0.2));
      border-radius: 6px;
      padding: 16px 20px;
      margin-bottom: 20px;
    }
    .section-title {
      font-weight: 600;
      font-size: 1rem;
      margin-bottom: 8px;
    }
    .section-desc {
      font-size: 0.85rem;
      color: var(--vscode-descriptionForeground);
      margin-bottom: 12px;
    }
    .flex-row {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    input[type="text"], input[type="number"], select {
      background: var(--vscode-input-background);
      color: var(--vscode-input-foreground);
      border: 1px solid var(--vscode-input-border, rgba(127, 127, 127, 0.4));
      padding: 6px 10px;
      border-radius: 4px;
      font-size: 0.9rem;
      outline: none;
    }
    input[type="text"]:focus, input[type="number"]:focus, select:focus {
      border-color: var(--vscode-focusBorder);
    }
    input[type="text"] {
      flex: 1;
    }
    button {
      background: var(--vscode-button-background);
      color: var(--vscode-button-foreground);
      border: none;
      padding: 7px 16px;
      border-radius: 4px;
      cursor: pointer;
      font-weight: 500;
      font-size: 0.9rem;
    }
    button:hover {
      background: var(--vscode-button-hoverBackground);
    }
    .btn-secondary {
      background: var(--vscode-button-secondaryBackground);
      color: var(--vscode-button-secondaryForeground);
    }
    .btn-secondary:hover {
      background: var(--vscode-button-secondaryHoverBackground);
    }
    .checkbox-group {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
      margin-top: 8px;
    }
    .checkbox-label {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .btn-submit {
      width: 100%;
      padding: 10px;
      font-size: 1rem;
      margin-top: 10px;
    }
    .tip-box {
      font-size: 0.85rem;
      padding: 10px 14px;
      background: rgba(30, 144, 255, 0.1);
      border-left: 3px solid #1e90ff;
      border-radius: 4px;
      margin-top: 18px;
    }
  </style>
</head>
<body>
  <h2>⚙️ Identity Generator Setup</h2>
  <div class="subtitle">Configure your default settings. You only need to do this once. Afterwards, use <code>identity generate</code> directly in your terminal.</div>

  <form id="prefsForm">
    <!-- 1. Location -->
    <div class="section">
      <div class="section-title">1. Default Output Location</div>
      <div class="section-desc">Folder where generated Excel, JSON, and CSV files will be stored.</div>
      <div class="flex-row">
        <input type="text" id="defaultLocation" value="${prefs.defaultLocation}" required />
        <button type="button" class="btn-secondary" onclick="browseFolder()">Browse...</button>
      </div>
    </div>

    <!-- 2. Subfolder -->
    <div class="section">
      <div class="section-title">2. Generated Folder Name</div>
      <div class="section-desc">Automatic subfolder name created inside the output location.</div>
      <input type="text" id="folderName" value="${prefs.folderName}" style="width: 240px;" required />
    </div>

    <!-- 3. Default Fields -->
    <div class="section">
      <div class="section-title">3. Default Fields</div>
      <div class="section-desc">Select which fields should be generated when --fields is omitted:</div>
      <div class="checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" id="field_name" ${hasName ? 'checked' : ''} /> Full Name
        </label>
        <label class="checkbox-label">
          <input type="checkbox" id="field_email" ${hasEmail ? 'checked' : ''} /> Email Address
        </label>
        <label class="checkbox-label">
          <input type="checkbox" id="field_password" ${hasPass ? 'checked' : ''} /> Secure Password
        </label>
        <label class="checkbox-label">
          <input type="checkbox" id="field_phone" ${hasPhone ? 'checked' : ''} /> Reserved Phone (+1 555-01xx)
        </label>
      </div>
    </div>

    <!-- 4. Default Quantity & Format -->
    <div class="section">
      <div class="section-title">4. Default Quantity & Format</div>
      <div class="section-desc">Initial defaults for <code>identity generate</code>:</div>
      <div class="flex-row" style="gap: 24px;">
        <div>
          <label style="display: block; font-size: 0.85rem; margin-bottom: 4px;">Quantity (Default: 1):</label>
          <input type="number" id="defaultQuantity" value="${prefs.defaultQuantity}" min="1" max="10000" style="width: 100px;" required />
        </div>
        <div>
          <label style="display: block; font-size: 0.85rem; margin-bottom: 4px;">Format (Default: Terminal):</label>
          <select id="defaultFormat" style="width: 140px;">
            <option value="terminal" ${prefs.defaultFormat === 'terminal' ? 'selected' : ''}>Terminal</option>
            <option value="excel" ${prefs.defaultFormat === 'excel' ? 'selected' : ''}>Excel (.xlsx)</option>
            <option value="json" ${prefs.defaultFormat === 'json' ? 'selected' : ''}>JSON (.json)</option>
            <option value="csv" ${prefs.defaultFormat === 'csv' ? 'selected' : ''}>CSV (.csv)</option>
          </select>
        </div>
      </div>
    </div>

    <button type="submit" class="btn-submit">Save Preferences & Complete Setup</button>
  </form>

  <div class="tip-box">
    💡 <strong>Tip:</strong> After saving, open any VS Code integrated terminal and type <code>identity generate</code> or <code>identity man</code>.
  </div>

  <script>
    const vscode = acquireVsCodeApi();

    function browseFolder() {
      vscode.postMessage({ command: 'browseFolder' });
    }

    window.addEventListener('message', event => {
      const message = event.data;
      if (message.command === 'setFolder') {
        document.getElementById('defaultLocation').value = message.path;
      }
    });

    document.getElementById('prefsForm').addEventListener('submit', (e) => {
      e.preventDefault();

      const fields = [];
      if (document.getElementById('field_name').checked) fields.push('name');
      if (document.getElementById('field_email').checked) fields.push('email');
      if (document.getElementById('field_password').checked) fields.push('password');
      if (document.getElementById('field_phone').checked) fields.push('phone');

      if (fields.length === 0) {
        alert('Please select at least one default field.');
        return;
      }

      vscode.postMessage({
        command: 'savePreferences',
        data: {
          defaultLocation: document.getElementById('defaultLocation').value,
          folderName: document.getElementById('folderName').value,
          defaultQuantity: document.getElementById('defaultQuantity').value,
          defaultFormat: document.getElementById('defaultFormat').value,
          defaultFields: fields
        }
      });
    });
  </script>
</body>
</html>`;
  }
}
