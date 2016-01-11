class FileItemsController < ApplicationController
  def index
    @file_items = FileItem.all
  end

  def new
    @file_item = FileItem.new
  end

  def create
    @file_item = FileItem.new(file_item_params)

    if @file_item.save
      format.html { redirect_to file_items_index_path, flash[:success] = "The file #{@file_item.name} has been uplaoded" }
      format.json { head :no_content }
    else
      render "new"
    end

  end

  def destroy
    @file_item = FileItem.find(params[:id])
    @file_item.destroy
    format.html { redirect_to file_items_path, flash[:danger] = "The file #{@file_item.name} has been deleted" }
    format.json {}
  end

  private
    def file_item_params
      params.require(:file_item).permit(:name, :attachment)
    end
end
