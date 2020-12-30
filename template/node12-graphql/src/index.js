import { GraphQLClient } from 'graphql-request';
import app from '@launchql/openfaas-job-fn';
import env from './env';
import handler from './function/handler';

app.post('*', async (req, res, next) => {
  try {

    const databaseId = req.get('X-Database-Id');
    const jobId = req.get('X-Job-Id');

    const client = new GraphQLClient(
      env.GRAPHQL_URL, {
        headers: {
          'X-Api-Name': 'private',
          'X-Database-Id': databaseId
        }
      }
    );  

    const jobs = new GraphQLClient(
      env.GRAPHQL_URL, {
        headers: {
          'X-Api-Name': 'jobs',
          'X-Database-Id': databaseId
        }
      }
    );  

    const meta = new GraphQLClient(
      env.GRAPHQL_URL, {
        headers: {
          'X-Meta-Schema': true,
          'X-Database-Id': databaseId
        }
      }
    );  

    const result = await handler(req.body, {
      jobId,
      databaseId,
      client,
      jobs,
      meta
    });
    
    res.status(200).json(result);

  } catch (e) {
    next(e);
  }
});

app.listen(env.PORT);
