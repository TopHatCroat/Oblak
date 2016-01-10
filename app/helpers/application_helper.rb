module ApplicationHelper

  def full_title(page_title = '')
    base_title = "Project Oblak"
    if page_title.empty?
      base_title
    end
    else
      page_title + " | " + base_title
  end
end
