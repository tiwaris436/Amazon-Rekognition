import boto3
import json
import sys


#Analyzes videos using the Rekognition Video API 
class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    queueUrl = ''
    roleArn = ''
    topicArn = ''
    bucket = ''
    video = 'Shocking illusion - Pretty celebrities turn ugly!.mp4'
    

    #Entry point. Starts analysis of video in specified bucket.
    def main(self):

        jobFound = False
        sqs = boto3.client('sqs')
       
        # Change active start function for the desired analysis. Also change the GetResults function later in this code.
        #=====================================

        response = self.rek.start_face_detection(Video={'S3Object':{'Bucket':self.bucket,'Name':self.video}},
            NotificationChannel={'RoleArn':self.roleArn, 'SNSTopicArn':self.topicArn},FaceAttributes='ALL' )
        

       
        #=====================================
        print('Start Job Id: ' + response['JobId'])
        dotLine=0
        while jobFound == False:
            sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:
                
                if 'Messages' not in sqsResponse:
                    if dotLine<20:
                        print('.')
                        dotLine=dotLine+1
                    else:
                        print()
                        dotLine=0    
                    sys.stdout.flush()
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        #Change to match the start function earlier in this code.
                        #=============================================
                        self.GetResultsFaces(rekMessage['JobId'])                     
                                                
                        #=============================================

                        sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])

        print('done')

    # Gets the results of face detection by calling GetFaceDetection. Face 
    # detection is started by calling StartFaceDetection.
    # jobId is the identifier returned from StartFaceDetection
    def GetResultsFaces(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False

        while finished == False:
            response = self.rek.get_face_detection(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken)

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for faceDetection in response['Faces']:
                print('Face: ' + str(faceDetection['Face']['Emotions']))
                print('Confidence: ' + str(faceDetection['Face']['Confidence']))
                print('Timestamp: ' + str(faceDetection['Timestamp']))
                print()

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

if __name__ == "__main__":

    analyzer=VideoDetect()
    analyzer.main()
