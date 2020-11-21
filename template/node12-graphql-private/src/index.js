import app from '@launchql/openfaas-job-fn';
import env from './env';
import { client, jobsClient } from './client';
import handler from './function/handler';

app.post('*', async (req, res, next) => {
  try {
    const result = await handler(req.body, {
      client,
      jobsClient
    });
    res.status(200).json(result);
  } catch (e) {
    next(e);
  }
});

app.listen(env.PORT);
