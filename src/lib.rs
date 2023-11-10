use pyo3::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Range {
    start: usize,
    end: usize,
}

impl Range {
    pub fn new(start: usize, end: usize) -> Self {
        assert!(start < end);
        Self { start, end }
    }
}

#[derive(Debug, Clone)]
struct Node<T>(Option<T>)
where
    T: Clone + std::ops::Add<Output = T>;

impl<T> Node<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    fn new(value: T) -> Self {
        Self(Some(value))
    }
}

impl<T> std::ops::Add for Node<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        if let Some(self_value) = self.0 {
            if let Some(rhs_value) = rhs.0 {
                return Self(Some(self_value + rhs_value));
            }

            return Self(Some(self_value));
        }

        if let Some(rhs_value) = rhs.0 {
            return Self(Some(rhs_value));
        }

        Self(None)
    }
}

#[derive(Debug, PartialEq)]
pub enum TreeType {
    Sum,
    Max,
    Min,
}

#[derive(Debug, Clone)]
pub struct SegmentTree<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    container: Vec<Node<T>>,
    len: usize,
    len_next_power_of_two: usize,
}

impl<T> SegmentTree<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn build_from(slices: &[T]) -> Self {
        let len = slices.len();

        let len_next_power_of_two = len.next_power_of_two();

        let container: Vec<_> = {
            let mut container: Vec<_> = std::iter::repeat(Node(None))
                .take(len_next_power_of_two - 1)
                .chain(slices.iter().cloned().map(Node::new))
                .chain(std::iter::repeat(Node(None)).take(len_next_power_of_two - len))
                .collect();

            for index in (0..(len_next_power_of_two - 1)).rev() {
                let left_child_index = 2 * index + 1;
                container[index] =
                    container[left_child_index].clone() + container[left_child_index + 1].clone();
            }

            container
        };

        Self {
            container,
            len,
            len_next_power_of_two,
        }
    }

    pub fn update(&mut self, value: T, at: usize) {
        assert!(at < self.len);
        let mut at = at + self.len_next_power_of_two - 1;
        self.container[at] = Node(Some(value));

        while at > 0 {
            at -= 1;
            let parent_index = at / 2;

            self.container[parent_index] =
                self.container[(at ^ 1) + 1].clone() + self.container[at + 1].clone();

            at = parent_index;
        }
    }

    pub fn query(&self, range: Range) -> Option<T> {
        if range.end > self.len {
            return None;
        }

        self._query(
            0,
            range,
            Range {
                start: 0,
                end: self.len_next_power_of_two,
            },
        )
        .0
    }

    #[inline]
    fn _query(&self, node_index: usize, range: Range, current_range: Range) -> Node<T> {
        let mut nodes_stack = vec![(node_index, current_range)];
        let mut query = Node(None);

        while let Some((
            node_index,
            Range {
                start: current_start,
                end: current_end,
            },
        )) = nodes_stack.pop()
        {
            if current_start >= range.end || current_end <= range.start {
                continue;
            }

            if current_start >= range.start && current_end <= range.end {
                query = query + self.container[node_index].clone();
                continue;
            }

            let current_middle = (current_start + current_end) / 2;
            let left_child_index = 2 * node_index + 1;

            nodes_stack.push((
                left_child_index + 1,
                Range {
                    start: current_middle,
                    end: current_end,
                },
            ));

            nodes_stack.push((
                left_child_index,
                Range {
                    start: current_start,
                    end: current_middle,
                },
            ));
        }

        query
    }
}

impl<T> SegmentTree<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    fn take_from(container: Vec<Node<T>>, len: usize, len_next_power_of_two: usize) -> Self {
        Self {
            container,
            len,
            len_next_power_of_two,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Min<T>(T)
where
    T: Clone + PartialOrd;

impl<T> Min<T>
where
    T: Clone + PartialOrd,
{
    pub fn new(value: T) -> Self {
        Self(value)
    }

    pub fn value(&self) -> &T {
        &self.0
    }
}

impl<T> std::ops::Add for Min<T>
where
    T: Clone + PartialOrd,
{
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        if self.0 < rhs.0 {
            return Self(self.0);
        }

        Self(rhs.0)
    }
}

#[derive(Debug, Clone)]
pub struct Max<T>(T)
where
    T: Clone + PartialOrd;

impl<T> Max<T>
where
    T: Clone + PartialOrd,
{
    pub fn new(value: T) -> Self {
        Self(value)
    }

    pub fn value(&self) -> &T {
        &self.0
    }
}

impl<T> std::ops::Add for Max<T>
where
    T: Clone + PartialOrd,
{
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        if self.0 > rhs.0 {
            return Self(self.0);
        }

        Self(rhs.0)
    }
}

#[derive(Debug, Clone)]
pub struct Sum<T>(T)
where
    T: Clone + std::ops::Add<Output = T>;

impl<T> Sum<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    pub fn new(value: T) -> Self {
        Self(value)
    }

    pub fn value(&self) -> &T {
        &self.0
    }
}

impl<T> std::ops::Add for Sum<T>
where
    T: Clone + std::ops::Add<Output = T>,
{
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self(self.0 + rhs.0)
    }
}

#[pyfunction]
pub fn build_sum_tree(arr: Vec<isize>) -> PySegmentTree {
    let len = arr.len();

    let tree = {
        let data: Vec<_> = arr.into_iter().map(Sum).collect();
        SegmentTree::build_from(&data)
    };

    let container: Vec<_> = tree
        .container
        .into_iter()
        .map(|x| x.0)
        .map(|x| x.map(|x| x.0))
        .collect();

    PySegmentTree {
        container,
        len,
        tree_type: TreeType::Sum,
    }
}

#[pyfunction]
pub fn build_min_tree(arr: Vec<isize>) -> PySegmentTree {
    let len = arr.len();

    let tree = {
        let data: Vec<_> = arr.into_iter().map(Min).collect();
        SegmentTree::build_from(&data)
    };

    let container: Vec<_> = tree
        .container
        .into_iter()
        .map(|x| x.0)
        .map(|x| x.map(|x| x.0))
        .collect();

    PySegmentTree {
        container,
        len,
        tree_type: TreeType::Min,
    }
}

#[pyfunction]
pub fn build_max_tree(arr: Vec<isize>) -> PySegmentTree {
    let len = arr.len();

    let tree = {
        let data: Vec<_> = arr.into_iter().map(Max).collect();
        SegmentTree::build_from(&data)
    };

    let container: Vec<_> = tree
        .container
        .into_iter()
        .map(|x| x.0)
        .map(|x| x.map(|x| x.0))
        .collect();

    PySegmentTree {
        container,
        len,
        tree_type: TreeType::Max,
    }
}

#[pyclass]
pub struct PySegmentTree {
    container: Vec<Option<isize>>,
    len: usize,
    tree_type: TreeType,
}

#[pymethods]
impl PySegmentTree {
    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn container(&self) -> Vec<Option<isize>> {
        self.container.clone()
    }

    pub fn query_sum(&self, ranges: Vec<(usize, usize)>) -> Vec<isize> {
        assert_eq!(self.tree_type, TreeType::Sum);

        let tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Sum))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        let mut queries = Vec::with_capacity(ranges.len());
        for (start, end) in ranges {
            let range = Range::new(start, end);
            queries.push(tree.query(range));
        }

        queries.into_iter().map(|x| x.unwrap().0).collect()
    }

    pub fn query_min(&self, ranges: Vec<(usize, usize)>) -> Vec<isize> {
        assert_eq!(self.tree_type, TreeType::Min);

        let tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Min))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        let mut queries = Vec::with_capacity(ranges.len());
        for (start, end) in ranges {
            let range = Range::new(start, end);
            queries.push(tree.query(range));
        }

        queries.into_iter().map(|x| x.unwrap().0).collect()
    }

    pub fn query_max(&self, ranges: Vec<(usize, usize)>) -> Vec<isize> {
        assert_eq!(self.tree_type, TreeType::Max);

        let tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Max))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        let mut queries = Vec::with_capacity(ranges.len());
        for (start, end) in ranges {
            let range = Range::new(start, end);
            queries.push(tree.query(range));
        }

        queries.into_iter().map(|x| x.unwrap().0).collect()
    }

    pub fn update_sum(&mut self, values_n_indexes: Vec<(isize, usize)>) {
        assert_eq!(self.tree_type, TreeType::Sum);

        let mut tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Sum))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        for (value, index) in values_n_indexes.into_iter() {
            tree.update(Sum(value), index);
        }

        self.container = tree
            .container
            .into_iter()
            .map(|x| x.0)
            .map(|x| x.map(|x| x.0))
            .collect();
    }

    pub fn update_max(&mut self, values_n_indexes: Vec<(isize, usize)>) {
        assert_eq!(self.tree_type, TreeType::Max);

        let mut tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Max))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        for (value, index) in values_n_indexes.into_iter() {
            tree.update(Max(value), index);
        }

        self.container = tree
            .container
            .into_iter()
            .map(|x| x.0)
            .map(|x| x.map(|x| x.0))
            .collect();
    }

    pub fn update_min(&mut self, values_n_indexes: Vec<(isize, usize)>) {
        assert_eq!(self.tree_type, TreeType::Min);

        let mut tree = {
            let container: Vec<_> = self
                .container
                .clone()
                .into_iter()
                .map(|x| x.map(Min))
                .map(Node)
                .collect();
            let len_next_power_of_two = self.len.next_power_of_two();
            SegmentTree::take_from(container, self.len, len_next_power_of_two)
        };

        for (value, index) in values_n_indexes.into_iter() {
            tree.update(Min(value), index);
        }

        self.container = tree
            .container
            .into_iter()
            .map(|x| x.0)
            .map(|x| x.map(|x| x.0))
            .collect();
    }
}

#[pyfunction]
pub fn tree_container_indexes_manager(tree_len: usize) -> Vec<Option<(usize, usize)>> {
    let len_next_power_of_two = tree_len.next_power_of_two();
    let mut manager: Vec<Option<(usize, usize)>> = std::iter::repeat(None)
        .take(len_next_power_of_two - 1)
        .chain((0..).zip(1..).take(tree_len).map(Some))
        .chain(std::iter::repeat(None).take(len_next_power_of_two - tree_len))
        .collect();
    for index in (0..(len_next_power_of_two - 1)).rev() {
        let left_child_index = 2 * index + 1;
        // let left_index = manager[left_child_index].map(|x| x.0);
        // let right_index = manager[left_child_index + 1].map(|x| x.1);

        match (manager[left_child_index], manager[left_child_index + 1]) {
            (Some(left), Some(right)) => manager[index] = Some((left.0, right.1)),
            (Some(left), None) => manager[index] = Some(left),
            (None, Some(right)) => manager[index] = Some(right),
            _ => manager[index] = None,
        };
    }

    manager
}

#[pymodule]
#[pyo3(name = "segment_tree")]
pub fn segment_tree(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(build_max_tree, m)?)?;
    m.add_function(wrap_pyfunction!(build_min_tree, m)?)?;
    m.add_function(wrap_pyfunction!(build_sum_tree, m)?)?;
    m.add_class::<PySegmentTree>()?;
    m.add_function(wrap_pyfunction!(tree_container_indexes_manager, m)?)?;
    Ok(())
}
