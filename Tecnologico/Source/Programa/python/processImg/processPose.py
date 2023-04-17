import cv2
from featureExtraction.poseModel import PosePoints

def processPose(image):
    '''Faz todo o processamento da imagem'''
    try:
        points = poseEstimation(image)
        #Desenha os traços
        image = draw_pose(image, points, (000,000,255), PosePoints.Pose.CORPO)
        image = draw_pose(image, points, (255,000,000), PosePoints.Pose.BRACO_DIR)
        image = draw_pose(image, points, (255,000,000), PosePoints.Pose.BRACO_ESQ)
        image = draw_pose(image, points, (000,255,000), PosePoints.Pose.PERNA_DIR)
        image = draw_pose(image, points, (000,255,000), PosePoints.Pose.PERNA_ESQ)
        return image
    except:
        return image

def poseEstimation(image):
    '''A partir de uma imagem faz a estimativa de pose da mesma retornando os keyPoints'''
    #dimensão da img
    hight, width, _ = image.shape
    pose = PosePoints.getPose(image)
    aux = PosePoints(hight, width, pose)
    points = aux.getPoints()
    return points

def draw_pose(image,points,color,pose):
    '''Desenha o Segmento na imagem a partir dos pontos de referencia'''
    pose_to_segment = {
        PosePoints.Pose.BRACO_DIR: PosePoints.Segmento.BRACO_DIR,
        PosePoints.Pose.BRACO_ESQ: PosePoints.Segmento.BRACO_ESQ,
        PosePoints.Pose.PERNA_DIR: PosePoints.Segmento.PERNA_DIR,
        PosePoints.Pose.PERNA_ESQ: PosePoints.Segmento.PERNA_ESQ,
        PosePoints.Pose.CORPO    : PosePoints.Segmento.CORPO
    }
    cycle = (pose == PosePoints.Pose.CORPO)
    segment = pose_to_segment.get(pose)
    if segment is None:
        return image
    return draw_segment(image,points,segment,color,cycle)

def draw_segment(image,points,segment,color,cycle=False):
    '''Desenha um segmento, conectando pontos de referência em sequência'''
    # Copia a imagem
    img = image.copy()
    # Obtém as poses do segmento
    poses = segment.value

    # Desenha uma linha entre cada par de poses consecutivas
    for i in range( len(poses)-1 ):
        start, end = points[poses[i]], points[poses[i+1]]
        cv2.line(img, start, end, color)
    # Desenha uma linha entre a última e a primeira pose, caso cycle=True
    if cycle:
        start, end = points[poses[-1]], points[poses[0]]
        cv2.line(img, start, end, color)
    return img