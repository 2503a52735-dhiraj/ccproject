"""
Full Generator for Lab Assignment:
Comparative Evaluation of AI Code Generation Tools (GitHub Copilot, ChatGPT, Claude)
Produces:
1. AI_Tools_Comparative_Evaluation_Assignment.docx (Professional Word document)
2. AI_Tools_Comparative_Evaluation_Assignment.html (Interactive, print-ready HTML report)
3. landing_copilot.html (Representative Copilot generated landing page)
4. landing_chatgpt.html (Representative ChatGPT generated landing page)
5. landing_claude.html (Representative Claude generated landing page)
"""

import os
import zipfile
import xml.sax.saxutils as saxutils

def esc(text):
    if text is None:
        return ""
    return saxutils.escape(str(text))

class DocxBuilder:
    def __init__(self):
        self.body_elements = []

    def add_title_block(self, title, subtitle, metadata_items):
        # Decorative top border / banner
        xml = f"""
        <w:p>
          <w:pPr>
            <w:jc w:val="center"/>
            <w:spacing w:before="200" w:after="100"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="40"/>
              <w:color w:val="0F172A"/>
            </w:rPr>
            <w:t>{esc(title)}</w:t>
          </w:r>
        </w:p>
        <w:p>
          <w:pPr>
            <w:jc w:val="center"/>
            <w:spacing w:before="0" w:after="240"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:sz w:val="24"/>
              <w:color w:val="2563EB"/>
            </w:rPr>
            <w:t>{esc(subtitle)}</w:t>
          </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

        # Metadata table box
        rows_xml = []
        for label, val in metadata_items:
            rows_xml.append(f"""
            <w:tr>
              <w:tc>
                <w:tcPr>
                  <w:tcW w:w="3000" w:type="dxa"/>
                  <w:shd w:fill="F1F5F9"/>
                </w:tcPr>
                <w:p>
                  <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
                  <w:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                      <w:b/>
                      <w:sz w:val="20"/>
                      <w:color w:val="1E293B"/>
                    </w:rPr>
                    <w:t>{esc(label)}</w:t>
                  </w:r>
                </w:p>
              </w:tc>
              <w:tc>
                <w:tcPr>
                  <w:tcW w:w="6360" w:type="dxa"/>
                  <w:shd w:fill="FFFFFF"/>
                </w:tcPr>
                <w:p>
                  <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
                  <w:r>
                    <w:rPr>
                      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                      <w:sz w:val="20"/>
                      <w:color w:val="334155"/>
                    </w:rPr>
                    <w:t>{esc(val)}</w:t>
                  </w:r>
                </w:p>
              </w:tc>
            </w:tr>
            """)

        meta_table = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9360" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="6" w:color="CBD5E1"/>
              <w:left w:val="single" w:sz="6" w:color="CBD5E1"/>
              <w:bottom w:val="single" w:sz="6" w:color="CBD5E1"/>
              <w:right w:val="single" w:sz="6" w:color="CBD5E1"/>
              <w:insideH w:val="single" w:sz="4" w:color="E2E8F0"/>
              <w:insideV w:val="single" w:sz="4" w:color="E2E8F0"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="80" w:type="dxa"/>
              <w:bottom w:w="80" w:type="dxa"/>
              <w:left w:w="140" w:type="dxa"/>
              <w:right w:w="140" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid>
            <w:gridCol w:w="3000"/>
            <w:gridCol w:w="6360"/>
          </w:tblGrid>
          {"".join(rows_xml)}
        </w:tbl>
        <w:p><w:pPr><w:spacing w:before="120" w:after="160"/></w:pPr></w:p>
        """
        self.body_elements.append(meta_table)

    def add_heading_1(self, text):
        xml = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="360" w:after="120"/>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="16" w:space="4" w:color="2563EB"/>
            </w:pBdr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="32"/>
              <w:color w:val="1E3A8A"/>
            </w:rPr>
            <w:t>{esc(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_heading_2(self, text):
        xml = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="260" w:after="100"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="26"/>
              <w:color w:val="1E40AF"/>
            </w:rPr>
            <w:t>{esc(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_heading_3(self, text):
        xml = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="180" w:after="60"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="23"/>
              <w:color w:val="0F172A"/>
            </w:rPr>
            <w:t>{esc(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def add_paragraph(self, text, bold_prefix=None, italic=False):
        runs = []
        if bold_prefix:
            runs.append(f"""
            <w:r>
              <w:rPr>
                <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                <w:b/>
                <w:sz w:val="22"/>
                <w:color w:val="0F172A"/>
              </w:rPr>
              <w:t xml:space="preserve">{esc(bold_prefix)} </w:t>
            </w:r>
            """)
        runs.append(f"""
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            {"<w:i/>" if italic else ""}
            <w:sz w:val="22"/>
            <w:color w:val="334155"/>
          </w:rPr>
          <w:t xml:space="preserve">{esc(text)}</w:t>
        </w:r>
        """)
        xml = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="40" w:after="100" w:line="276" w:lineRule="auto"/>
          </w:pPr>
          {"".join(runs)}
        </w:p>
        """
        self.body_elements.append(xml)

    def add_bullet(self, text, bold_prefix=None):
        runs = []
        runs.append(f"""
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/>
            <w:sz w:val="22"/>
            <w:color w:val="2563EB"/>
          </w:rPr>
          <w:t xml:space="preserve">▪  </w:t>
        </w:r>
        """)
        if bold_prefix:
            runs.append(f"""
            <w:r>
              <w:rPr>
                <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                <w:b/>
                <w:sz w:val="22"/>
                <w:color w:val="0F172A"/>
              </w:rPr>
              <w:t xml:space="preserve">{esc(bold_prefix)} </w:t>
            </w:r>
            """)
        runs.append(f"""
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:sz w:val="22"/>
            <w:color w:val="334155"/>
          </w:rPr>
          <w:t xml:space="preserve">{esc(text)}</w:t>
        </w:r>
        """)
        xml = f"""
        <w:p>
          <w:pPr>
            <w:ind w:left="400" w:hanging="200"/>
            <w:spacing w:before="30" w:after="60" w:line="260" w:lineRule="auto"/>
          </w:pPr>
          {"".join(runs)}
        </w:p>
        """
        self.body_elements.append(xml)

    def add_callout(self, text, title="KEY INSIGHT"):
        xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9360" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="none"/>
              <w:left w:val="single" w:sz="28" w:space="0" w:color="2563EB"/>
              <w:bottom w:val="none"/>
              <w:right w:val="none"/>
              <w:insideH w:val="none"/>
              <w:insideV w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="120" w:type="dxa"/>
              <w:bottom w:w="120" w:type="dxa"/>
              <w:left w:w="200" w:type="dxa"/>
              <w:right w:w="200" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid>
            <w:gridCol w:w="9360"/>
          </w:tblGrid>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="9360" w:type="dxa"/>
                <w:shd w:fill="EFF6FF"/>
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:spacing w:before="40" w:after="40"/>
                </w:pPr>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="22"/>
                    <w:color w:val="1D4ED8"/>
                  </w:rPr>
                  <w:t xml:space="preserve">[{esc(title)}] </w:t>
                </w:r>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:sz w:val="22"/>
                    <w:color w:val="1E293B"/>
                  </w:rPr>
                  <w:t>{esc(text)}</w:t>
                </w:r>
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>
        <w:p><w:pPr><w:spacing w:before="60" w:after="80"/></w:pPr></w:p>
        """
        self.body_elements.append(xml)

    def add_code_block(self, code_text):
        lines = code_text.strip().split("\n")
        paragraphs = []
        for line in lines:
            paragraphs.append(f"""
            <w:p>
              <w:pPr>
                <w:spacing w:before="0" w:after="0" w:line="230" w:lineRule="auto"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                  <w:sz w:val="18"/>
                  <w:color w:val="0F172A"/>
                </w:rPr>
                <w:t xml:space="preserve">{esc(line)}</w:t>
              </w:r>
            </w:p>
            """)
        
        xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9360" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:insideH w:val="none"/>
              <w:insideV w:val="none"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="100" w:type="dxa"/>
              <w:bottom w:w="100" w:type="dxa"/>
              <w:left w:w="160" w:type="dxa"/>
              <w:right w:w="160" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid>
            <w:gridCol w:w="9360"/>
          </w:tblGrid>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="9360" w:type="dxa"/>
                <w:shd w:fill="F8FAFC"/>
              </w:tcPr>
              {"".join(paragraphs)}
            </w:tc>
          </w:tr>
        </w:tbl>
        <w:p><w:pPr><w:spacing w:before="60" w:after="80"/></w:pPr></w:p>
        """
        self.body_elements.append(xml)

    def add_table(self, headers, rows, col_widths=None):
        num_cols = len(headers)
        total_w = 9360
        if not col_widths:
            col_w = total_w // num_cols
            col_widths = [col_w] * num_cols

        grid_cols = "".join([f'<w:gridCol w:w="{w}"/>' for w in col_widths])

        header_cells = []
        for i, h in enumerate(headers):
            header_cells.append(f"""
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="{col_widths[i]}" w:type="dxa"/>
                <w:shd w:fill="1E3A8A"/>
                <w:vAlign w:val="center"/>
              </w:tcPr>
              <w:p>
                <w:pPr>
                  <w:spacing w:before="70" w:after="70"/>
                  <w:jc w:val="center"/>
                </w:pPr>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                    <w:b/>
                    <w:sz w:val="21"/>
                    <w:color w:val="FFFFFF"/>
                  </w:rPr>
                  <w:t>{esc(h)}</w:t>
                </w:r>
              </w:p>
            </w:tc>
            """)

        rows_xml = [f"""
        <w:tr>
          <w:trPr>
            <w:tblHeader/>
          </w:trPr>
          {"".join(header_cells)}
        </w:tr>
        """]

        for row_idx, row in enumerate(rows):
            bg_color = "FFFFFF" if row_idx % 2 == 0 else "F8FAFC"
            row_cells = []
            for col_idx, cell in enumerate(row):
                is_bold = (col_idx == 0) or ("Total" in str(row[0])) or ("Rank" in str(row[0]))
                align = "center" if (col_idx in [1, 2, 3, 4] and len(str(cell)) <= 12) else "left"
                row_cells.append(f"""
                <w:tc>
                  <w:tcPr>
                    <w:tcW w:w="{col_widths[col_idx]}" w:type="dxa"/>
                    <w:shd w:fill="{bg_color}"/>
                    <w:vAlign w:val="center"/>
                  </w:tcPr>
                  <w:p>
                    <w:pPr>
                      <w:spacing w:before="50" w:after="50"/>
                      <w:jc w:val="{align}"/>
                    </w:pPr>
                    <w:r>
                      <w:rPr>
                        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                        {"<w:b/>" if is_bold else ""}
                        <w:sz w:val="20"/>
                        <w:color w:val="1E293B"/>
                      </w:rPr>
                      <w:t>{esc(cell)}</w:t>
                    </w:r>
                  </w:p>
                </w:tc>
                """)
            rows_xml.append(f"""
            <w:tr>
              {"".join(row_cells)}
            </w:tr>
            """)

        xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="{total_w}" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
              <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
              <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            </w:tblBorders>
            <w:tblCellMar>
              <w:top w:w="80" w:type="dxa"/>
              <w:bottom w:w="80" w:type="dxa"/>
              <w:left w:w="120" w:type="dxa"/>
              <w:right w:w="120" w:type="dxa"/>
            </w:tblCellMar>
          </w:tblPr>
          <w:tblGrid>
            {grid_cols}
          </w:tblGrid>
          {"".join(rows_xml)}
        </w:tbl>
        <w:p><w:pPr><w:spacing w:before="60" w:after="80"/></w:pPr></w:p>
        """
        self.body_elements.append(xml)

    def add_page_break(self):
        xml = """
        <w:p>
          <w:r>
            <w:br w:type="page"/>
          </w:r>
        </w:p>
        """
        self.body_elements.append(xml)

    def build(self, output_path):
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

        styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="22"/>
        <w:color w:val="1E293B"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>"""

        document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {"".join(self.body_elements)}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/>
    </w:sectPr>
  </w:body>
</w:document>"""

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx:
            docx.writestr("[Content_Types].xml", content_types)
            docx.writestr("_rels/.rels", rels)
            docx.writestr("word/_rels/document.xml.rels", doc_rels)
            docx.writestr("word/styles.xml", styles)
            docx.writestr("word/document.xml", document)

        print(f"Built DOCX: {output_path} ({os.path.getsize(output_path)} bytes)")

print("DocxBuilder initialized successfully.")
