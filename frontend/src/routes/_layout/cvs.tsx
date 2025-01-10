import {
  Container,
  Heading,
  SkeletonText,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"
import { z } from "zod"

import { CvsService } from "../../client"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"
import AddCV from "../../components/CVs/AddCV"
import { PaginationFooter } from "../../components/Common/PaginationFooter.tsx"

const cvsSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/cvs") ({
 component: CVs,
    validateSearch: (search) => cvsSearchSchema.parse(search),
})

const PER_PAGE = 5

function getCVsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      CvsService.readCvs({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["cvs", { page }],
  }
}

function CVsTable() {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const setPage = (page: number) =>
    navigate({ search: (prev: {[key: string]: string}) => ({ ...prev, page }) })

  const {
    data: cvs,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getCVsQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && cvs?.data.length === PER_PAGE
  const hasPreviousPage = page > 1

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getCVsQueryOptions({ page: page + 1 }))
    }
  }, [page, queryClient, hasNextPage])

  return (
    <>
      <TableContainer>
        <Table size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th>Recipient</Th>
              <Th>Edited At</Th>
              <Th>Created At</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          {isPending ? (
            <Tbody>
              <Tr>
                {new Array(5).fill(null).map((_, index) => (
                  <Td key={index}>
                    <SkeletonText noOfLines={1} paddingBlock="16px" />
                  </Td>
                ))}
              </Tr>
            </Tbody>
          ) : (
            <Tbody>
              {cvs?.data.map((cv) => (
                <Tr key={cv.id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Td>{cv.name}</Td>
                  <Td>{cv.recipient}</Td>
                  <Td>{new Date(cv.edited_at).toLocaleString()}</Td>
                  <Td>{new Date(cv.created_at).toLocaleString()}</Td>
                  <Td>
                    <ActionsMenu type={"CV"} value={cv} />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          )}
        </Table>
      </TableContainer>
      <PaginationFooter
        page={page}
        onChangePage={setPage}
        hasNextPage={hasNextPage}
        hasPreviousPage={hasPreviousPage}
      />
    </>
  )
}

function CVs() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        CVs Management
      </Heading>

      <Navbar type={"CV"} addModalAs={AddCV} />
      <CVsTable />
    </Container>
  )
}
