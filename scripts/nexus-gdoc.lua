-- YAML values are parsed as Markdown, so text like "<placeholder>" becomes raw HTML that
-- stringify would drop. Keep raw HTML as literal text.
local function stringify(value)
  if pandoc.utils.type(value) == "Inlines" then
    value = value:walk({ RawInline = function(raw) return pandoc.Str(raw.text) end })
  end
  return pandoc.utils.stringify(value)
end

local function html_escape(value)
  return (value
    :gsub("&", "&amp;")
    :gsub("<", "&lt;")
    :gsub(">", "&gt;")
    :gsub('"', "&quot;")
    :gsub("'", "&#39;"))
end

local function metadata(meta, key)
  local value = meta[key]
  if value == nil then
    error("Missing required YAML metadata: " .. key)
  end
  return html_escape(stringify(value))
end

-- Optional field: a string, or a YAML list joined with `separator`. Returns nil when absent or empty.
local function optional(meta, key, separator)
  local value = meta[key]
  if value == nil then
    return nil
  end
  local items = {}
  if value.t == "MetaList" or pandoc.utils.type(value) == "List" then
    for _, item in ipairs(value) do
      local text = stringify(item)
      if text ~= "" then
        table.insert(items, html_escape(text))
      end
    end
  else
    local text = stringify(value)
    if text ~= "" then
      items = { html_escape(text) }
    end
  end
  if #items == 0 then
    return nil
  end
  return table.concat(items, separator)
end

local function row(label, value)
  return '<tr><th scope="row"><strong>' .. label .. "</strong></th><td>" .. value .. "</td></tr>"
end

function Pandoc(doc)
  local title = metadata(doc.meta, "title")
  local slug = metadata(doc.meta, "slug")
  local description = metadata(doc.meta, "meta-description")

  -- Prevent Pandoc from adding a duplicate title block before the metadata table.
  doc.meta.title = nil

  local rows = {
    row("Judul Artikel", title),
    row("Slug", slug),
    row("Meta Description", description),
  }
  for _, field in ipairs({
    { "Main Keyword", "main-keyword", ", " },
    { "Related Keywords", "related-keywords", ", " },
    -- One bullet per note: Docs keeps <br> as cell paragraphs, but read_file_content runs them together.
    { "Notes", "notes", "</li><li>", "<ul><li>", "</li></ul>" },
  }) do
    local value = optional(doc.meta, field[2], field[3])
    if value then
      table.insert(rows, row(field[1], (field[4] or "") .. value .. (field[5] or "")))
    end
  end

  local html = table.concat({
    "<table>",
    '<colgroup><col style="width:28.846%"><col style="width:71.154%"></colgroup>',
    "<tbody>",
    table.concat(rows),
    "</tbody>",
    "</table>",
  })

  local parsed = pandoc.read(html, "html")
  local metadata_table = parsed.blocks[1]
  if metadata_table == nil or metadata_table.t ~= "Table" then
    error("Failed to build the metadata table")
  end

  metadata_table.colspecs = {
    { pandoc.AlignLeft, 0.28846 },
    { pandoc.AlignLeft, 0.71154 },
  }
  table.insert(doc.blocks, 1, metadata_table)
  return doc
end
