import {
  AfterViewInit,
  Component,
  ElementRef,
  OnDestroy,
  ViewChild
} from '@angular/core';

import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { python } from '@codemirror/lang-python'
import { EditorState } from '@codemirror/state'
import { indentWithTab } from '@codemirror/commands';
import { autocompletion, CompletionContext} from '@codemirror/autocomplete'

@Component({
  selector: 'app-editor',
  imports: [],
  templateUrl: './editor.html',
  styleUrl: './editor.css'
})
export class Editor implements AfterViewInit, OnDestroy {
  @ViewChild('editor', { static: true })
  editorElement!: ElementRef<HTMLDivElement>;

  private view?: EditorView;

  ngAfterViewInit(): void {
    this.view = new EditorView({ 
      state: this.createEditorState(),
      parent: this.editorElement.nativeElement,
    });
  }  
  ngOnDestroy(): void {
    this.view?.destroy();
  }  


  private createEditorState(): EditorState {

    return EditorState.create({ 
      doc : "Test",
      extensions: [ 
          basicSetup,
          python(),
          keymap.of([indentWithTab]),
          EditorView.lineWrapping,
          autocompletion({
            override: [this.pythonCompletions.bind(this)]
          })
      ]
    });
  }  

  getCode(): string {
    return this.view?.state.doc.toString() ?? '';
  }

  setCode(code: string): void {
    if(!this.view) return;

    this.view.dispatch({
      changes: {
        from: 0,
        to: this.view?.state.doc.length,
        insert: code
        
      }
    });
  }

  private async pythonCompletions(context: CompletionContext) {
    const word = context.matchBefore(/[\w.]*/);

    if (!word) {
      return null;
    }

    const line = context.state.doc.lineAt(context.pos);

    const response = await fetch(
      'http://localhost:8000/api/python/completions',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          code: context.state.doc.toString(),
          line: line.number - 1,
          character: context.pos - line.from
        })
      }
    );

    const items = await response.json();

    return {
      from: word.from,
      options: items.map((item: any) => ({
        label: item.label,
        type: item.type,
        detail: item.detail,
        info: item.documentation,
        apply: item.insertText
      }))
    };
  }



}
