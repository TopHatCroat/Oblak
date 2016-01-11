class User < ActiveRecord::Base
  attr_accessor :remember_token               # with this and appropriate functions we are recreating the principle behind has_secure_password ie. remember the stuff without saving it into the database
  before_save { self.email = email.downcase } #supposed to verify that the fuckers are unique for sure
                                              #before_save is a callback, guess when it gets called

  validates :name,  presence: true, length: { maximum: 255 }

  VALID_EMAIL_REGEX = /\A[\w+\-.]+@[a-z\d\-.]+\.[a-z]+\z/i
  validates :email, presence: true, length: { maximum: 255 }, format: { with: VALID_EMAIL_REGEX }, uniqueness: true


  #uz has_secure_password možeš koristit 2 virtualna polja "password" i "password_confirmation"
  #koje automatski prepoznaje kao šifre i radi hash na njima
  has_secure_password
  validates :password, presence: true, length: { minimum: 6 }

  has_many :file_items, dependent: :destroy
  accepts_nested_attributes_for :file_items


  # Returns the hash digest of the given string.
  def User.digest(string)
    cost = ActiveModel::SecurePassword.min_cost ? BCrypt::Engine::MIN_COST : BCrypt::Engine.cost
    BCrypt::Password.create(string, cost: cost)
  end

  # Returns random token
  def User.new_token
    SecureRandom.urlsafe_base64
  end

  # Remembers a user in the database for use in persistent sessions.
  def remember
    self.remember_token = User.new_token
    update_attribute(:remember_digest, User.digest(remember_token))
  end

  # Returns true if the given token matches the digest
  def authenticated?(remember_token)
    return false if remember_digest.nil?
    BCrypt::Password.new(remember_digest).is_password?(remember_token)
  end

  # Forget user ie. clears remember_digest atribute in the table users for this user
  def forget
    update_attribute(:remember_digest, nil)
  end
end
