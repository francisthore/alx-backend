import sinon from 'sinon';
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  const logger = sinon.spy(console);
  const queue = createQueue({ name: 'push_notification_code_test' });

  before(() => {
    queue.testMode.enter(true);
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  afterEach(() => {
    logger.log.resetHistory();
  });

  it('throws an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('adds jobs to the queue with the correct type', (done) => {
    expect(queue.testMode.jobs.length).to.equal(0);
    const jobs = [
      { phoneNumber: '44556677889', message: 'Use the code 1982 to verify your account' },
      { phoneNumber: '98877665544', message: 'Use the code 1738 to verify your account' },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    queue.process('push_notification_code_3', () => {
      expect(logger.log.calledWith('Notification job created:', queue.testMode.jobs[0].id)).to.be.true;
      done();
    });
  });

  it('handles the progress event for a job', (done) => {
    queue.testMode.jobs[0].addListener('progress', () => {
      expect(logger.log.calledWith('Notification job', queue.testMode.jobs[0].id, '25% complete')).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('progress', 25);
  });

  it('handles the failed event for a job', (done) => {
    queue.testMode.jobs[0].addListener('failed', () => {
      expect(logger.log.calledWith('Notification job', queue.testMode.jobs[0].id, 'failed:', 'Failed to send')).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('failed', new Error('Failed to send'));
  });

  it('handles the complete event for a job', (done) => {
    queue.testMode.jobs[0].addListener('complete', () => {
      expect(logger.log.calledWith('Notification job', queue.testMode.jobs[0].id, 'completed')).to.be.true;
      done();
    });
    queue.testMode.jobs[0].emit('complete');
  });
});
