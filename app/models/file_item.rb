class FileItem < ActiveRecord::Base
  mount_uploader :attachment, AttachmentUploader

  validates :name, presence: true
  validates :user, presence: true

  belongs_to :user


  before_save :update_file_item_attributes

  private

  def update_file_item_attributes
    if !name.present?
      self.name = 'asad'
    end

    # if model.present? && asset_changed?
    #   self.content_type = asset.file.content_type
    #   self.size = asset.file.size
    # end
  end
end
