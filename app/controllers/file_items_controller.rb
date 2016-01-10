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
      redirect_to user_file_item_path, notice: "The file #{@file_item.name} has been uplaoded"
    else
      render "new"
    end

  end

  def destroy
    @file_item = FileItem.find(params[:id])
    @file_item.destroy
    redirect_to recumes_path, notice: "The file #{@file_item.name} has been deleted"
  end

  private
    def file_item_params
      params.require(:file_item).permit(:name, :attachment)
    end
end
