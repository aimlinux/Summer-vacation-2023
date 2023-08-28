from skimage.metrics import structural_similarity as compare_ssim
import cv2

def calculate_similarity(image1_path, image2_path):
    # 画像読み込み
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # 画像をグレースケールに変換
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    
    #画像のサイズが一致するか確認
    if gray_image1.shape != gray_image2.shape:
        #raise ValueError("Input images must have the same dimensions.")
        return 10
    
    # 画像の類似度を計算
    similarity = compare_ssim(gray_image1, gray_image2)
    
    return similarity

if __name__ == "__main__":
    image1_path = "test/AI/image/img_1.png"  # 1つ目の画像ファイルのパス
    image2_path = "test/AI/image/img_2.png"  # 2つ目の画像ファイルのパス
    
    similarity_percentage = calculate_similarity(image1_path, image2_path)
    if similarity_percentage == 10:
        print("Error")
    else:
        print(f"画像の類似度: {similarity_percentage:.2%}")