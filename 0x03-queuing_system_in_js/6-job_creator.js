import kue from 'kue';

const queue = kue.createQueue();

const jobObj = {
  phoneNumber: '07898768988',
  message: 'Hello there you are a winner',
};

const job = queue
  .create('push_notification_code', jobObj)
  .save((err) => {
    if (!err) {
      console.log(`Notification job created: ${job.id}`);
    }
  });

job
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed', () => {
    console.log('Notification job failed');
  });
