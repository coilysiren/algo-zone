// this script is a duplicate of sort_builtin
// it's only real purpose is to help test out rust toolchain

fn main() {
    let mut vec = vec![1, 5, 10, 2, 15];

    vec.sort();

    assert_eq!(vec, vec![1, 2, 5, 10, 15]);
}
