class UsersController < ApplicationController
  def new
  end

  def show
    @user = User.find(params[:id])
    @files = @user.file_items.all
  end

  def new #ako ovaj pogled prođe izvršava se "create"
    @user = User.new
  end

  def create
    @user = User.new(user_params)
    if @user.save
      log_in @user
      flash[:success] = "Welcome to the Oblak project!"
      redirect_to @user #equivalent: redirect_to user_url(@user)
    else
      render 'new' #ako je fejlo vrati ga na početak tj. na new
    end
  end

  private
    def user_params
      params.require(:user).permit(:name, :email, :password, :password_confirmation)
    end
end
