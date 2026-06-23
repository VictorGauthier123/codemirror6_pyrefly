import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  ViewChild
} from '@angular/core';

import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import { EditorState } from '@codemirror/state';
import { indentWithTab } from '@codemirror/commands';
import { LSPClient, Transport, languageServerExtensions } from '@codemirror/lsp-client';

@Component({
  selector: 'app-editor',
  imports: [],
  templateUrl: './editor.html',
  styleUrl: './editor.css'
})

// Creation of the codemirror IDE class
export class Editor implements AfterViewInit, OnDestroy {
  @ViewChild('editor', { static: true })
  editorElement!: ElementRef<HTMLDivElement>;

  private view?: EditorView; // code mirror instance
  private socket?: WebSocket; // backend websocket connection
  private client?: LSPClient; // LSP client for code mirror
  private readonly fileUri = 'file:///main.py'; // 

  async ngAfterViewInit(): Promise<void> {
    const transport = await this.createTransport('ws://localhost:8000/lsp'); // we open the websocket connection with the backend

    // creation of the LSP client of codemirror branched to the websocket
    this.client = new LSPClient({
      rootUri: this.fileUri,
      extensions: languageServerExtensions(),
    }).connect(transport);
    
    // main idea of code mirror, view allow to have a visual "IDE" having state as all the informations it needs
    this.view = new EditorView({
      state: this.createEditorState(),
      parent: this.editorElement.nativeElement,
    });
  }

  ngOnDestroy(): void {
    this.view?.destroy();
    this.client?.disconnect();
    this.socket?.close();
  }

  // creation of the state 
  private createEditorState(): EditorState {
    return EditorState.create({
      doc: 'import numpy as np\n\nnp.', // the original text in the editor
      extensions: [ // all the features we need
        basicSetup,
        python(),
        keymap.of([indentWithTab]),
        EditorView.lineWrapping,
        this.client?.plugin(this.fileUri, 'python') ?? [] //branch to the LSP client
      ]
    });
  }

  // receive the code in the editor
  getCode(): string {
    return this.view?.state.doc.toString() ?? '';
  }

  // set the code in the editor. Will allow for instance to fill with the autocompletion
  setCode(code: string): void {
    if (!this.view) return;

    this.view.dispatch({
      changes: {
        from: 0,
        to: this.view.state.doc.length,
        insert: code
      }
    });
  }
  // adapter between the websocket and codemirror lsp client
  private createTransport(uri: string): Promise<Transport> {
    // we do a promise because we need to wait that the websocket is open
    return new Promise((resolve, reject) => {
      let handlers: Array<(value: string) => void> = [];
      const socket = new WebSocket(uri);
      // we call this.socket in order to destroy it at the end
      this.socket = socket;
      socket.onmessage = (event) => {
        for (const handler of handlers) {
          handler(event.data.toString());
        }
      };
      socket.onerror = () => reject(new Error('LSP websocket connection failed'));
      socket.onopen = () => resolve({
        // send is a method from @automirror/lsp-client in order to send message to the backend. Send the JSON in the websocket
        send(message: string) {
          socket.send(message);
        },
        subscribe(handler: (value: string) => void) {
          handlers.push(handler);
        },
        unsubscribe(handler: (value: string) => void) {
          handlers = handlers.filter((current) => current !== handler);
        }
      });
    });
  }
}
