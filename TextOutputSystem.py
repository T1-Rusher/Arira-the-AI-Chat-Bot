"""
✍️ Text Output System - AI के लिए Writing/Text Generation
Various formats में text generate करता है
"""

from datetime import datetime
import json
import re

class TextOutputSystem:
    def __init__(self):
        """Text Output System को initialize करें"""
        self.output_history = []
        self.templates = {}
        self.writing_styles = {
            'formal': {
                'vocabulary': 'advanced',
                'tone': 'professional',
                'structure': 'organized'
            },
            'casual': {
                'vocabulary': 'simple',
                'tone': 'friendly',
                'structure': 'conversational'
            },
            'technical': {
                'vocabulary': 'specialized',
                'tone': 'precise',
                'structure': 'detailed'
            },
            'creative': {
                'vocabulary': 'varied',
                'tone': 'expressive',
                'structure': 'flexible'
            }
        }
        
    def generate_text(self, content, output_format='plain', style='casual'):
        """
        Text generate करें
        
        Args:
            content: Generate करने के लिए content
            output_format: Output format (plain, markdown, html, json)
            style: Writing style
        """
        formatted_output = self._format_output(content, output_format)
        styled_output = self._apply_style(formatted_output, style)
        
        output = {
            'content': content,
            'formatted_output': styled_output,
            'format': output_format,
            'style': style,
            'word_count': len(content.split()),
            'character_count': len(content),
            'timestamp': datetime.now().isoformat()
        }
        
        self.output_history.append(output)
        return output
    
    def _format_output(self, content, format_type):
        """Content को specific format में convert करें"""
        if format_type == 'markdown':
            return self._to_markdown(content)
        elif format_type == 'html':
            return self._to_html(content)
        elif format_type == 'json':
            return json.dumps({'content': content}, ensure_ascii=False, indent=2)
        else:  # plain
            return content
    
    def _to_markdown(self, content):
        """Markdown format में convert करें"""
        # Add markdown formatting
        lines = content.split('\n')
        markdown = []
        
        for line in lines:
            if line.strip():
                # Simple heading detection
                if len(line) < 50 and not line.endswith('.'):
                    markdown.append(f"## {line}")
                else:
                    markdown.append(line)
            else:
                markdown.append('')
        
        return '\n'.join(markdown)
    
    def _to_html(self, content):
        """HTML format में convert करें"""
        lines = content.split('\n')
        html = ['<div class="ai-output">']
        
        for line in lines:
            if line.strip():
                html.append(f'  <p>{line}</p>')
        
        html.append('</div>')
        return '\n'.join(html)
    
    def _apply_style(self, content, style):
        """Writing style apply करें"""
        if style not in self.writing_styles:
            return content
        
        style_config = self.writing_styles[style]
        
        # Style-based modifications (simplified)
        if style == 'formal':
            # Add formal phrases
            content = content.replace('नहीं', 'नहीं है')
        elif style == 'casual':
            # Keep it simple
            pass
        
        return content
    
    def write_paragraph(self, topic, sentences=3, style='casual'):
        """Paragraph लिखें"""
        paragraph = f"{topic} "
        
        for i in range(sentences):
            paragraph += f"यह {topic} के बारे में वाक्य {i+1} है। "
        
        return self.generate_text(paragraph, output_format='plain', style=style)
    
    def write_list(self, items, format_type='markdown'):
        """List बनाएं"""
        if format_type == 'markdown':
            list_text = '\n'.join([f"- {item}" for item in items])
        elif format_type == 'html':
            list_text = '<ul>\n' + '\n'.join([f'  <li>{item}</li>' for item in items]) + '\n</ul>'
        else:
            list_text = '\n'.join([f"{i+1}. {item}" for i, item in enumerate(items)])
        
        return self.generate_text(list_text, output_format=format_type)
    
    def write_report(self, title, sections, style='formal'):
        """Report लिखें"""
        report = f"# {title}\n\n"
        
        for section_title, section_content in sections.items():
            report += f"## {section_title}\n\n"
            report += f"{section_content}\n\n"
        
        return self.generate_text(report, output_format='markdown', style=style)
    
    def write_email(self, recipient, subject, body, tone='formal'):
        """Email draft करें"""
        email = f"""प्रिय {recipient},

विषय: {subject}

{body}

सादर,
AI Assistant
"""
        return self.generate_text(email, output_format='plain', style=tone)
    
    def write_code_comment(self, code_snippet, language='python'):
        """Code comments generate करें"""
        comment_styles = {
            'python': '#',
            'javascript': '//',
            'java': '//',
            'html': '<!--'
        }
        
        comment_char = comment_styles.get(language, '#')
        
        commented_code = f"""{comment_char} Auto-generated comment
{comment_char} This code performs: [function description]

{code_snippet}"""
        
        return self.generate_text(commented_code, output_format='plain')
    
    def summarize_text(self, long_text, max_sentences=3):
        """Text को summarize करें"""
        sentences = re.split(r'[.!?]+', long_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Take first N sentences as summary (simplified)
        summary = '. '.join(sentences[:max_sentences]) + '.'
        
        return self.generate_text(summary, output_format='plain')
    
    def translate_style(self, text, from_style, to_style):
        """एक style से दूसरे में convert करें"""
        # Simplified translation
        if from_style == 'casual' and to_style == 'formal':
            text = text.replace('हाँ', 'जी हाँ')
            text = text.replace('नहीं', 'जी नहीं')
        
        return self.generate_text(text, style=to_style)
    
    def expand_abbreviations(self, text):
        """Text में abbreviations को expand करें"""
        abbrev_map = {
            'AI': 'Artificial Intelligence',
            'ML': 'Machine Learning',
            'NLP': 'Natural Language Processing',
            'API': 'Application Programming Interface'
        }
        
        expanded = text
        for abbr, full in abbrev_map.items():
            expanded = expanded.replace(abbr, full)
        
        return self.generate_text(expanded, output_format='plain')
    
    def format_table(self, headers, rows, format_type='markdown'):
        """Table format करें"""
        if format_type == 'markdown':
            table = '| ' + ' | '.join(headers) + ' |\n'
            table += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
            for row in rows:
                table += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
        elif format_type == 'html':
            table = '<table>\n  <tr>\n'
            table += ''.join([f'    <th>{h}</th>\n' for h in headers])
            table += '  </tr>\n'
            for row in rows:
                table += '  <tr>\n'
                table += ''.join([f'    <td>{cell}</td>\n' for cell in row])
                table += '  </tr>\n'
            table += '</table>'
        else:
            # Plain text table
            col_widths = [max(len(str(h)), max(len(str(row[i])) for row in rows)) for i, h in enumerate(headers)]
            table = ' | '.join(h.ljust(w) for h, w in zip(headers, col_widths)) + '\n'
            table += '-+-'.join(['-' * w for w in col_widths]) + '\n'
            for row in rows:
                table += ' | '.join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + '\n'
        
        return self.generate_text(table, output_format=format_type)
    
    def get_statistics(self):
        """Output statistics"""
        if not self.output_history:
            return {'total_outputs': 0}
        
        total_words = sum(o['word_count'] for o in self.output_history)
        formats = [o['format'] for o in self.output_history]
        styles = [o['style'] for o in self.output_history]
        
        return {
            'total_outputs': len(self.output_history),
            'total_words': total_words,
            'formats_used': dict((f, formats.count(f)) for f in set(formats)),
            'styles_used': dict((s, styles.count(s)) for s in set(styles)),
            'average_length': total_words / len(self.output_history)
        }


# Example Usage
if __name__ == "__main__":
    print("=" * 70)
    print("✍️ TEXT OUTPUT SYSTEM DEMO")
    print("=" * 70)
    
    tos = TextOutputSystem()
    
    # Basic text generation
    print("\n1. Basic Text Generation:")
    output = tos.generate_text("यह एक simple text output है।", style='casual')
    print(f"   Output: {output['formatted_output']}")
    print(f"   Words: {output['word_count']}")
    
    # Paragraph writing
    print("\n2. Paragraph Writing:")
    para = tos.write_paragraph("Artificial Intelligence", sentences=3, style='formal')
    print(f"   {para['formatted_output'][:80]}...")
    
    # List creation
    print("\n3. List Creation (Markdown):")
    items = ["Item 1", "Item 2", "Item 3"]
    list_output = tos.write_list(items, format_type='markdown')
    print(list_output['formatted_output'])
    
    # Email writing
    print("\n4. Email Draft:")
    email = tos.write_email("Rajesh", "Meeting Reminder", "कल की meeting 3 PM पर है।", tone='formal')
    print(email['formatted_output'][:100] + "...")
    
    # Table formatting
    print("\n5. Table Formatting:")
    headers = ['Name', 'Age', 'City']
    rows = [['Raj', '25', 'Delhi'], ['Priya', '28', 'Mumbai']]
    table = tos.format_table(headers, rows, format_type='markdown')
    print(table['formatted_output'])
    
    # Statistics
    print("\n6. Statistics:")
    stats = tos.get_statistics()
    print(f"   Total outputs: {stats['total_outputs']}")
    print(f"   Total words: {stats['total_words']}")
