import gql from 'graphql-tag';

// example GQL 
const GetUsers = gql`
  query GetUsers {
    users {
      nodes {
        id
        username
      }
    }
  }
`;

export default async (params, context) => {
  const { client } = context;
  // example query
  const apiInfo = await client.query({
    query: GetUsers
  });

  // return whatever you want
  return {
    works: true,
    apiInfo,
    ...params
  };
};
