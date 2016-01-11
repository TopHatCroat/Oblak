class FileItemsController < ApplicationController
  def index
    @file_items = FileItem.all
  end

  def new
    @file_item = FileItem.new
  end

  def create
    @file_item = FileItem.new(file_item_params)

    respond_to do |format|
      if @picture.save
        format.html { redirect_to file_items_index_path, flash[:success] = "The file #{@file_item.name} has been uplaoded" }
        format.json { render json: @file_item, status: :created, location: @file_item }
      else
        format.html { render action: "new" }
        format.json { render json: @file_item.errors, status: :unprocessable_entity }
      end
    end
  end
  #
  #   #check if file is within picture_path
  #   if params[:attachment]
  #     #picture_path_params = params[:picture][:picture_path]
  #     #create a new tempfile named fileupload
  #     tempfile = Tempfile.new("fileupload")
  #     tempfile.binmode
  #     #get the file and decode it with base64 then write it to the tempfile
  #     tempfile.write(Base64.decode64(params["attachemnt"]))
  #
  #     #create a new uploaded file
  #     uploaded_file = ActionDispatch::Http::UploadedFile.new(:tempfile => tempfile, :filename => picture_path_params["filename"], :original_filename => picture_path_params["original_filename"])
  #
  #     #replace picture_path with the new uploaded file
  #     params[:file_item] =  uploaded_file
  #
  #   end
  #
  #   @picture = Picture.new(params[:picture])
  #
  #   respond_to do |format|
  #     if @picture.save
  #       format.html { redirect_to @picture, notice: 'Picture was successfully created.' }
  #       format.json { render json: @picture, status: :created, location: @picture }
  #     else
  #       format.html { render action: "new" }
  #       format.json { render json: @picture.errors, status: :unprocessable_entity }
  #     end
  #   end
  # end


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
