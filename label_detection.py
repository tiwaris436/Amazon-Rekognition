import boto3
import json
import sys

#Analyzes videos using the Rekognition Video API 
class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    queueUrl = 'https://sqs.us-west-1.amazonaws.com/997332955142/Video'
    roleArn = 'arn:aws:iam::997332955142:role/Rekognition_SNS'
    topicArn = 'arn:aws:sns:us-west-1:997332955142:AmazonRekognition'
    bucket = 'mlbucket9'
    video = 'Skate 3_ 50,000 points in 30 seconds in the MEGA PARK - YouTube (720p).mp4'

    #Entry point. Starts analysis of video in specified bucket.
    def main(self):

        jobFound = False
        sqs = boto3.client('sqs')
       
        # Change active start function for the desired analysis. Also change the GetResults function later in this code.
        #=====================================
        response = self.rek.start_label_detection(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                         NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.topicArn})


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
                        self.GetResultsLabels(rekMessage['JobId'])                   
                                                
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


    # Gets the results of labels detection by calling GetLabelDetection. Label
    # detection is started by a call to StartLabelDetection.
    # jobId is the identifier returned from StartLabelDetection
    def GetResultsLabels(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False

        while finished == False:
            response = self.rek.get_label_detection(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken,
                                            SortBy='TIMESTAMP')

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for labelDetection in response['Labels']:
                print(labelDetection['Label']['Name'])
                print(labelDetection['Label']['Confidence'])
                print(str(labelDetection['Timestamp']))

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

   



if __name__ == "__main__":

    analyzer=VideoDetect()
    analyzer.main()
