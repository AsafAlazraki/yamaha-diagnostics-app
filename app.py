def process_csv_to_tables(file_path, output_dir):
    try:
        print(f"Reading CSV file: {file_path}")
        sections = defaultdict(list)
        current_section = "Metadata"
        customer_name = "Unknown"
        
        # [Previous CSV reading code unchanged...]

        doc = Document()
        section = doc.sections[0]
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

        print("Available table styles:")
        for style in doc.styles:
            if style.type == 2:
                print(style.name)

        logo_path = os.path.join(os.path.dirname(__file__), "newlogo.png")
        if os.path.exists(logo_path):
            header = doc.sections[0].header
            logo_paragraph = header.add_paragraph()
            logo_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = logo_paragraph.add_run()
            run.add_picture(logo_path, width=Inches(3))
            doc.sections[0].header_distance = Inches(0.1)
        else:
            print(f"Error: logo.png not found at {logo_path}. Skipping logo.")

        # Add blank paragraph to create space between header and content
        spacer_paragraph = doc.add_paragraph()
        spacer_paragraph.space_after = Pt(20)  # Adds ~20pt (~0.28 inches) of space
        spacer_paragraph.space_before = Pt(0)   # No extra space above
        # Ensure the paragraph is empty and has no formatting
        for run in spacer_paragraph.runs:
            run.text = ""

        # Metadata section (center-aligned, no borders, larger text, no dotted line)
        if "Metadata" in sections:
            print("Processing Metadata section...")
            metadata_entries = []
            metadata_keys = [
                "YAMAHA DIAGNOSTIC SYSTEM", "Save date & time", "Customer name", 
                "Dealer name", "Number of engines", "Comment", "Model name", 
                "Engine serial number (PID number)", "ECM number"
            ]
            comment_value = "(empty)"
            i = 0
            while i < len(sections["Metadata"]):
                row = sections["Metadata"][i]
                if len(row) >= 1 and row[0].strip('"') in metadata_keys:
                    field = row[0].strip('"')
                    if field == "Comment":
                        if i + 1 < len(sections["Metadata"]) and not is_section_start(sections["Metadata"][i + 1]):
                            next_row = sections["Metadata"][i + 1]
                            comment_value = next_row[0].strip('"') if len(next_row) > 0 and next_row[0].strip('"') else "(empty)"
                            i += 1
                    else:
                        value = row[2].strip('"') if len(row) > 2 and row[2].strip('"') else row[1].strip('"') if len(row) > 1 and row[1].strip('"') != field else "(empty)"
                        display_field = "Service Date" if field == "Save date & time" else field
                        if field == "Dealer name":
                            value = "Northside Marine"
                        if value != "(empty)":
                            metadata_entries.append((display_field, value))
                i += 1
            if comment_value != "(empty)":
                metadata_entries.append(("Comment", comment_value))
            if total_engine_hours != "(empty)":
                metadata_entries.append(("Total Engine Hours", total_engine_hours))

            if metadata_entries:
                print(f"Creating Metadata table with {len(metadata_entries)} entries")
                num_rows = (len(metadata_entries) + 1) // 2
                table = doc.add_table(rows=num_rows, cols=2)
                table.style = 'Table Grid'
                remove_all_table_borders(table)  # Remove all borders (no dotted line)
                table.autofit = True
                for idx, (field, value) in enumerate(metadata_entries):
                    row_idx = idx // 2
                    col_idx = idx % 2
                    cell = table.cell(row_idx, col_idx)
                    paragraph = cell.paragraphs[0]
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run_field = paragraph.add_run(f"{field}: ")
                    run_field.bold = True
                    run_field.font.size = Pt(10)
                    run_value = paragraph.add_run(value)
                    run_value.bold = False
                    run_value.font.size = Pt(10)
                    paragraph.space_after = Pt(2)

        # [Rest of the function unchanged...]
