import 'cross-fetch/polyfill';
import env from './env';
import { ApolloClient, InMemoryCache } from '@apollo/client';

export const client = new ApolloClient({
  uri: env.GRAPHQL_URL,
  cache: new InMemoryCache()
});
