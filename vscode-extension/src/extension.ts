import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';
import { getPreferences } from './config';
import { SetupWebviewPanel } from './setupWebview';

export function activate(context: vscode.ExtensionContext) {
  // 1. Integrated Terminal Integration
  // Prepend extension bin directory to PATH for all integrated terminals in VS Code
  const binDir = path.join(context.extensionPath, 'bin');
  context.environmentVariableCollection.prepend('PATH', binDir + path.delimiter);

  // Prepend project src directory to PYTHONPATH so Python module identity_cli is discoverable
  const projectSrc = path.resolve(context.extensionPath, '..', 'src');
  if (fs.existsSync(projectSrc)) {
    context.environmentVariableCollection.prepend('PYTHONPATH', projectSrc + path.delimiter);
  }

  // 2. Register Commands
  const configureCommand = vscode.commands.registerCommand('identity.configure', () => {
    SetupWebviewPanel.render(context.extensionUri);
  });

  const manCommand = vscode.commands.registerCommand('identity.man', () => {
    const terminal = vscode.window.activeTerminal || vscode.window.createTerminal('Identity Generator');
    terminal.show();
    terminal.sendText('identity man');
  });

  const openTerminalCommand = vscode.commands.registerCommand('identity.openTerminal', () => {
    const terminal = vscode.window.createTerminal('Identity Generator');
    terminal.show();
    terminal.sendText('identity --help');
  });

  context.subscriptions.push(configureCommand, manCommand, openTerminalCommand);

  // 3. First-Time Setup Prompt
  const prefs = getPreferences();
  if (!prefs.setupCompleted) {
    vscode.window
      .showInformationMessage(
        'Welcome to Identity Generator! Configure your default location and preferences to get started.',
        'Configure Now',
        'Later'
      )
      .then((selection) => {
        if (selection === 'Configure Now') {
          SetupWebviewPanel.render(context.extensionUri);
        }
      });
  }
}

export function deactivate() {}
