import React, { useState, useEffect } from 'react';

type PaginatedTableProps = {
  data: any[];
  columns: { key: string; label: string }[];
  shipClassMap?: Record<string, string>;
  classColorMap?: Record<string, string>;
};

export default function PaginatedTable({
  data,
  columns,
  shipClassMap = {},
  classColorMap = {},
}: PaginatedTableProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [jumpToPage, setJumpToPage] = useState('');

  const totalPages = Math.ceil(data.length / rowsPerPage);

  const handleRowsPerPageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setRowsPerPage(Number(e.target.value));
    setCurrentPage(1);
  };

  const handleJumpInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setJumpToPage(e.target.value);
  };

  const handleJumpSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const page = Math.max(1, Math.min(totalPages, parseInt(jumpToPage, 10)));
    if (!isNaN(page)) {
      setCurrentPage(page);
    }
  };

  const currentData = data.slice(
    (currentPage - 1) * rowsPerPage,
    currentPage * rowsPerPage
  );

  useEffect(() => {
    setJumpToPage(String(currentPage));
  }, [currentPage]);

  return (
    <div>
      <div className='overflow-x-auto'>
        <table className='w-full border border-gray-300 text-sm'>
          <thead className='bg-gray-100'>
            <tr>
              {columns.map((col) => (
                <th
                  key={col.key}
                  className='px-3 py-2 text-left border-b border-gray-300'
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {currentData.map((row, i) => (
              <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                {columns.map((col) => {
                  let value = row[col.key];

                  if (col.key === 'class') {
                    const shipName = row['ship']?.split(' ')[0];
                    const className = shipClassMap[shipName] ?? 'Unknown Class';
                    const badgeClass =
                      classColorMap[className] ?? 'bg-gray-300 text-white';
                    value = (
                      <span
                        className={`inline-block rounded-sm px-2 py-1 text-xs font-bold ${badgeClass}`}
                      >
                        {className}
                      </span>
                    );
                  }

                  return (
                    <td
                      key={col.key}
                      className='px-3 py-2 border-b border-gray-200'
                    >
                      {col.key === 'class' ? (
                        <span
                          className={`inline-block rounded-sm px-2 py-1 text-xs font-bold ${
                            classColorMap[row[col.key]] ??
                            'bg-gray-300 text-white'
                          }`}
                        >
                          {row[col.key]}
                        </span>
                      ) : col.key === 'nextBonus' ? (
                        value || '—'
                      ) : (
                        value
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className='flex justify-center items-center gap-10 mt-6 flex-wrap'>
        {/* Results per page selector on the left side of the grouping */}
        <div>
          <label className='text-sm'>
            Results per page:{' '}
            <select
              value={rowsPerPage}
              onChange={handleRowsPerPageChange}
              className='border border-gray-300 px-2 py-1 text-sm rounded'
            >
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={30}>30</option>
            </select>
          </label>
        </div>

        {/* Page controls to the right of the selector */}
        <div className='flex items-center gap-4'>
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className='px-3 py-1 border rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50'
          >
            Prev
          </button>

          <form onSubmit={handleJumpSubmit} className='flex items-center gap-2'>
            <input
              type='number'
              value={jumpToPage}
              onChange={handleJumpInput}
              className='w-16 px-2 py-1 text-sm border border-gray-300 rounded'
              placeholder={`${currentPage}`}
              min={1}
              max={totalPages}
            />
            <span className='text-sm text-gray-900'>of {totalPages} pages</span>
          </form>

          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className='px-3 py-1 border rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50'
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
