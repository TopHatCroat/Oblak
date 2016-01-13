class FileItemsController < ApplicationController
  def index
    @file_items = @current_user.file_items.all
  end

  def new
    @user = User.find(session[:user_id])

    @file_item = @user.file_items.new

  end

  def create
    # if params[:attachment]
    #   #picture_path_params = params[:picture][:picture_path]
    #   #create a new tempfile named fileupload
    #   tempfile = Tempfile.new("fileupload")
    #   tempfile.binmode
    #   #get the file and decode it with base64 then write it to the tempfile
    #   tempfile.write(Base64.decode64(params["attachemnt"]))
    #
    #   #create a new uploaded file
    #   uploaded_file = ActionDispatch::Http::UploadedFile.new(:tempfile => tempfile, :filename => picture_path_params["filename"], :original_filename => picture_path_params["original_filename"])
    #
    #   #replace picture_path with the new uploaded file
    #   params[:file_item] =  uploaded_file

    @user = User.find(session[:user_id])

    @file_item = @user.file_items.new(file_item_params)

    @file_item.name = params[:original_filename] if @file_item.name == ""

    respond_to do |format|
      if @file_item.save
        format.html { redirect_to user_path @user.id, flash[:success] = "File has been uplaoded" }
        format.json { render json: @file_item, status: :created, location: @file_item }
      else
        format.html { render action: "new" }
        format.json { render json: @file_item.errors, status: :unprocessable_entity }
      end
    end
  end

  def destroy
    @user = User.find(session[:user_id])

    @file_item = FileItem.find(params[:id])
    @file_item.destroy
    respond_to do |format|

      format.html { redirect_to user_path @user.id, flash[:danger] = "File has been deleted" }
      format.json {render json: @file_item, status: :deleted}
    end
  end

  private
    def file_item_params
      params.require(:file_item).permit(:name, :attachment)
    end
end
